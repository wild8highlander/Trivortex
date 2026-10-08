-- SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
-- SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
-- ===========================================================================
-- TRIVORTEX — HASKELL VERIFICATION LADDER: DOUBLE VS EXACT-RATIONAL DUAL
-- ===========================================================================
-- Milestone M3 artifact. Provenance: a line-for-line port of the analytic
-- and numerical layers of `verification/trivortex/python/verify.py` (M0
-- release, repository main branch, commit 557bff8), plus the M3 flavor of
-- this port: the EXACT-RATIONAL DUAL RUN.
--
--   * The Double ladder re-implements checks V1–V4 in `Double` (same
--     formulas, same registered tolerance bands as README §6).
--   * The exact dual re-derives the four anchor values of the equilateral
--     reference state in the quadratic field ℚ(√3) — p + q·√3 with exact
--     `Rational` coefficients — where the identities P = 0, Q = 0, I = Γ
--     and H = 0 hold *by computation* (equality on ℚ(√3) is decidable
--     because √3 is irrational: p + q√3 = p' + q'√3 ⟺ p = p' ∧ q = q').
--
-- The library depends on nothing but `base` — the floating-point path is
-- exactly the platform's, with no library in between.
--
-- Author: Isaev Iskhak Khamzatovich (repository owner)
-- Year: 2026
-- ===========================================================================

module Trivortex.Verify
  ( -- presets and tolerances
    Preset(..)
  , presetQuick, presetDefault, presetFull
  , findPreset
    -- analytic layer (Theorem 3.1)
  , piD
  , analyticalFrequency, analyticalAmplitude, analyticalRadius
  , computeChaplygin
    -- numerical layer (Kirchhoff dynamics, RK4)
  , vortexRhs, rk4Step, invariants, equilateralInitial, lagrangeOmega
  , sideLengths
    -- the four checks
  , Check(..), Field(..)
  , checkV1, checkV2, checkV3, checkV4
    -- the ladder and the exact dual
  , LadderRun(..)
  , runLadder
  , ExactAnchor(..)
  , exactAnchors
  , QS(..)
    -- reporting
  , reportToJson, jsonFloat
  , utcNowIso, utcStamp
  , writeText, writeCsv
  , SvgSeries(..), svgLinePlot
  ) where

import Data.List (intercalate)
import Data.Ratio ((%))
import Foreign.Marshal.Alloc (allocaBytes)
import Foreign.Ptr (Ptr, nullPtr)
import Foreign.Storable (Storable(..))
import System.IO

-- ---------------------------------------------------------------------------
-- Presets (mirror of verify.py PRESETS)
-- ---------------------------------------------------------------------------

data Preset = Preset
  { presetName      :: String
  , presetRotations :: Int
  , presetSteps     :: Int
  , presetPoints    :: Int
  } deriving (Eq, Show)

presetQuick, presetDefault, presetFull :: Preset
presetQuick   = Preset "quick"   2  2000 200
presetDefault = Preset "default" 5  4000 1000
presetFull    = Preset "full"    20 8000 2000

findPreset :: String -> Maybe Preset
findPreset "quick"   = Just presetQuick
findPreset "default" = Just presetDefault
findPreset "full"    = Just presetFull
findPreset _         = Nothing

-- Registered tolerance bands (verification/README.md §6).
tolClosedForm, tolRk4, tolOmega :: Double
tolClosedForm = 1e-12   -- V1 residuals
tolRk4        = 1e-10   -- V2–V4 drifts
tolOmega      = 1e-6    -- measured omega

piD :: Double
piD = 3.14159265358979323846

-- ---------------------------------------------------------------------------
-- Section A — analytic layer (Theorem 3.1)
-- ---------------------------------------------------------------------------

-- | omega = (2π/T)·exp(C_Ch/π) — Theorem 3.1.
analyticalFrequency :: Double -> Double -> Double
analyticalFrequency c tPeriod = (2 * piD / tPeriod) * exp (c / piD)

-- | eps = 1/(exp(C_Ch/π) − 1); the document's guard returns 1 for C ≤ 0.01.
analyticalAmplitude :: Double -> Double
analyticalAmplitude c
  | c > 0.01  = 1 / (exp (c / piD) - 1)
  | otherwise = 1

-- | r_k(t) = √C_Ch·(1 + ε·cos(ω·t + 2πk/3)).
analyticalRadius :: Double -> Double -> Double -> Int -> Double
analyticalRadius t c tPeriod k =
  r0 * (1 + eps * cos (omega * t + 2 * piD * fromIntegral k / 3))
  where
    omega = analyticalFrequency c tPeriod
    eps   = analyticalAmplitude c
    r0    = if c > 0 then sqrt c else 0.01

-- | C_Ch = r²·(θ̇ − q·A_θ) with the gauge A_θ = 1/r.
computeChaplygin :: Double -> Double -> Double -> Double -> Double
computeChaplygin r thetaDot q aTheta =
  r * r * (thetaDot - q * a)
  where
    a | aTheta > 0 = aTheta
      | r > 0      = 1 / r
      | otherwise  = 0

-- | Python-style modulo: result in [0, m) for m > 0 (the separation check
-- of V1 relies on the lifted branch).
pythonMod :: Double -> Double -> Double
pythonMod x m =
  let r = x - m * fromIntegral (truncate (x / m) :: Integer)
  in if r < 0 then r + m else r

-- ---------------------------------------------------------------------------
-- Section B — numerical layer (Kirchhoff dynamics, RK4)
-- ---------------------------------------------------------------------------

-- | Kirchhoff right-hand side; state = flat [x0,y0,x1,y1,...].
--   dx_i/dt = −1/(2π) Σ_{j≠i} Γ_j (y_i − y_j)/r_ij²
--   dy_i/dt = +1/(2π) Σ_{j≠i} Γ_j (x_i − x_j)/r_ij²
vortexRhs :: [Double] -> [Double] -> [Double]
vortexRhs state gamma = concat [ [dx i, dy i] | i <- idx ]
  where
    n   = length gamma
    idx = [0 .. n - 1]
    pt i = (state !! (2 * i), state !! (2 * i + 1))
    r2 i j = let (xi, yi) = pt i
                 (xj, yj) = pt j
                 ddx = xi - xj
                 ddy = yi - yj
             in ddx * ddx + ddy * ddy
    dx i = sum [ negate (gamma !! j) * (snd (pt i) - snd (pt j)) / r2 i j / (2 * piD)
               | j <- idx, j /= i, r2 i j /= 0 ]
    dy i = sum [ gamma !! j * (fst (pt i) - fst (pt j)) / r2 i j / (2 * piD)
               | j <- idx, j /= i, r2 i j /= 0 ]

-- | One classical RK4 step.
rk4Step :: [Double] -> [Double] -> Double -> [Double]
rk4Step s g dt = zipWith4 combine s k1 k2 k3 k4
  where
    combine x a b c d = x + (dt / 6) * (a + 2 * b + 2 * c + d)
    half  = zipWith (\x k -> x + 0.5 * dt * k) s
    full  = zipWith (\x k -> x + dt * k) s
    k1 = vortexRhs s g
    k2 = vortexRhs (half k1) g
    k3 = vortexRhs (half k2) g
    k4 = vortexRhs (full k3) g

-- | H, P, Q, I — the classical (Chaplygin-type) vortex integrals.
invariants :: [Double] -> [Double] -> (Double, Double, Double, Double)
invariants state gamma = (h, p, q, imp)
  where
    n = length gamma
    pt i = (state !! (2 * i), state !! (2 * i + 1))
    dist i j = let (xi, yi) = pt i
                   (xj, yj) = pt j
               in sqrt ((xi - xj) * (xi - xj) + (yi - yj) * (yi - yj))
    h   = sum [ negate (gamma !! i * gamma !! j) * log (dist i j) / (2 * piD)
              | i <- [0 .. n - 1], j <- [i + 1 .. n - 1] ]
    p   = sum [ gamma !! i * fst (pt i) | i <- [0 .. n - 1] ]
    q   = sum [ gamma !! i * snd (pt i) | i <- [0 .. n - 1] ]
    imp = sum [ gamma !! i * (x * x + y * y) | i <- [0 .. n - 1], let (x, y) = pt i ]

-- | Three equal vortices on an equilateral triangle of side a.
equilateralInitial :: Double -> [Double]
equilateralInitial a =
  concat [ [r * cos ang, r * sin ang]
         | k <- [0 .. 2]
         , let ang = 2 * piD * fromIntegral k / 3 ]
  where r = a / sqrt 3

-- | omega = 3Γ/(2πa²) — the point-vortex Lagrange solution.
lagrangeOmega :: Double -> Double -> Double
lagrangeOmega gamma a = 3 * gamma / (2 * piD * a * a)

-- | Side lengths (01, 12, 20) of the triangle in `xy`.
sideLengths :: [Double] -> (Double, Double, Double)
sideLengths xy = (d 0 1, d 1 2, d 2 0)
  where
    d i j = let xi = xy !! (2 * i); yi = xy !! (2 * i + 1)
                xj = xy !! (2 * j); yj = xy !! (2 * j + 1)
            in sqrt ((xi - xj) * (xi - xj) + (yi - yj) * (yi - yj))

iterateN :: Int -> (a -> a) -> a -> a
iterateN n f = go n
  where
    go 0 x = x
    go k x = go (k - 1) (f x)

-- ---------------------------------------------------------------------------
-- The JSON-protocol value tree (schema of verification/README.md §12)
-- ---------------------------------------------------------------------------

data Field = FNum Double | FStr String | FBool Bool
           | FList [Field] | FMap [(String, Field)]

data Check = Check
  { checkName   :: String
  , checkFields :: [(String, Field)]
  , checkPassed :: Bool
  }

jsonEscape :: String -> String
jsonEscape = concatMap esc
  where
    esc '"'  = "\\\""
    esc '\\' = "\\\\"
    esc '\n' = "\\n"
    esc '\t' = "\\t"
    esc c    = [c]

jsonFloat :: Double -> String
jsonFloat v
  | isNaN v || isInfinite v = "null"
  | v == fromIntegral (round v :: Integer) && abs v < 1e16 =
      show (fromIntegral (round v :: Integer) :: Double)
  | otherwise = show v

fmtField :: Int -> Field -> String
fmtField ind f = case f of
  FNum x   -> jsonFloat x
  FStr s   -> '"' : jsonEscape s ++ "\""
  FBool b  -> if b then "true" else "false"
  FList xs -> "[\n" ++ intercalate ",\n"
                [ replicate (ind + 2) ' ' ++ fmtField (ind + 2) x | x <- xs ]
              ++ "\n" ++ replicate ind ' ' ++ "]"
  FMap ms  -> "{\n" ++ intercalate ",\n"
                [ replicate (ind + 2) ' ' ++ '"' : jsonEscape k
                  ++ "\": " ++ fmtField (ind + 2) v | (k, v) <- ms ]
              ++ "\n" ++ replicate ind ' ' ++ "}"

-- | Serialize the ladder run as the full JSON protocol report.
reportToJson :: String -> String -> String -> [Check] -> Double -> String
reportToJson suite preset dateUtc checks wall =
  "{\n"
  ++ "  \"suite\": \"" ++ jsonEscape suite ++ "\",\n"
  ++ "  \"version\": \"1.0\",\n"
  ++ "  \"preset\": \"" ++ jsonEscape preset ++ "\",\n"
  ++ "  \"date_utc\": \"" ++ jsonEscape dateUtc ++ "\",\n"
  ++ "  \"wall_time_s\": " ++ jsonFloat wall ++ ",\n"
  ++ "  \"checks_passed\": " ++ show (length (filter checkPassed checks)) ++ ",\n"
  ++ "  \"checks_total\": " ++ show (length checks) ++ ",\n"
  ++ "  \"all_passed\": " ++ (if all checkPassed checks then "true" else "false") ++ ",\n"
  ++ "  \"checks\": [\n"
  ++ intercalate ",\n"
       [ "    {\n"
         ++ intercalate ",\n"
              [ "      \"check\": \"" ++ jsonEscape (checkName c) ++ "\""
              , "      \"passed\": " ++ (if checkPassed c then "true" else "false") ]
              ++ concat [ ",\n      \"" ++ jsonEscape k ++ "\": "
                          ++ fmtField 6 v | (k, v) <- checkFields c ]
         ++ "\n    }"
       | c <- checks ]
  ++ "\n  ]\n}\n"

-- ---------------------------------------------------------------------------
-- UTC time via gettimeofday (both fields are `long` on LP64 Linux)
-- ---------------------------------------------------------------------------

data TimeVal = TimeVal !Int !Int

instance Storable TimeVal where
  sizeOf _    = 16
  alignment _ = 8
  peek p = do
    s <- peekByteOff p 0
    u <- peekByteOff p 8
    pure (TimeVal s u)
  poke p (TimeVal s u) = pokeByteOff p 0 s >> pokeByteOff p 8 u

foreign import ccall unsafe "gettimeofday"
  c_gettimeofday :: Ptr TimeVal -> Ptr () -> IO Int

utcParts :: IO (Int, Int, Int, Int, Int, Int)
utcParts = allocaBytes 16 $ \ptr -> do
  _ <- c_gettimeofday ptr nullPtr
  TimeVal secs usecs <- peek ptr
  let (y, mo, d, h, mi, s) = civilFromUnix secs
      fracSec = if usecs >= 500000 then s + 1 else s
  pure (y, mo, d, h, mi, fracSec)

civilFromUnix :: Int -> (Int, Int, Int, Int, Int, Int)
civilFromUnix secs = (y, mo, d, h, mi, s)
  where
    days = secs `div` 86400
    rem' = secs `mod` 86400
    h   = rem' `div` 3600
    mi  = (rem' `mod` 3600) `div` 60
    s   = rem' `mod` 60
    z   = days + 719468
    era = z `div` 146097
    doe = z - era * 146097
    yoe = (doe - doe `div` 1460 + doe `div` 36524 - doe `div` 146096) `div` 365
    y'  = yoe + era * 400
    doy = doe - (365 * yoe + yoe `div` 4 - yoe `div` 100)
    mp  = (5 * doy + 2) `div` 153
    d   = doy - (153 * mp + 2) `div` 5 + 1
    mo  = if mp < 10 then mp + 3 else mp - 9
    y   = if mo <= 2 then y' + 1 else y'

-- | UTC timestamp, Python-isoformat shape: 2026-10-08T02:39:07+00:00.
utcNowIso :: IO String
utcNowIso = do
  (y, mo, d, h, mi, s) <- utcParts
  pure (p4 y ++ "-" ++ p2 mo ++ "-" ++ p2 d ++ "T"
        ++ p2 h ++ ":" ++ p2 mi ++ ":" ++ p2 s ++ "+00:00")
  where p4 x = let t = show x in replicate (4 - length t) '0' ++ t

-- | UTC stamp for file names: 2026-10-08_02-39-07.
utcStamp :: IO String
utcStamp = do
  (y, mo, d, h, mi, s) <- utcParts
  pure (p4 y ++ "-" ++ p2 mo ++ "-" ++ p2 d ++ "_"
        ++ p2 h ++ "-" ++ p2 mi ++ "-" ++ p2 s)
  where p4 x = let t = show x in replicate (4 - length t) '0' ++ t

p2 :: Int -> String
p2 x = let t = show x in if length t < 2 then '0' : t else t

-- ---------------------------------------------------------------------------
-- The four checks
-- ---------------------------------------------------------------------------

-- | V1 — Theorem 3.1 closed form: choreography, periodicity, and the
-- recorded Section-6 drift diagnostic (C_Ch = 1, T = 2π, the ladder's
-- registered reference parameters).
checkV1 :: Int -> Check
checkV1 nPoints = Check
  "V1 Theorem 3.1: choreography + periodicity of the closed form"
  [ ("angular_separation_error",     FNum sepErr)
  , ("angular_separation_tolerance", FNum tolClosedForm)
  , ("periodicity_residual",         FNum perRes)
  , ("periodicity_tolerance",        FNum tolClosedForm)
  , ("section6_drift_diagnostic",    FNum drift)
  , ("params", FMap
      [ ("C_Ch", FNum 1.0)
      , ("T", FNum (2 * piD))
      , ("n_points", FNum (fromIntegral nPoints))
      , ("omega", FNum omega)
      , ("window", FStr "0..100T") ])
  ]
  (sepErr <= tolClosedForm && perRes <= tolClosedForm)
  where
    omega = analyticalFrequency 1.0 (2 * piD)
    tR    = 2 * piD / omega
    tMax  = 100 * 2 * piD
    ang k t = omega * t + 2 * piD * fromIntegral k / 3
    sepErr = maximum
      [ abs (pythonMod (ang (k + 1) t - ang k t) (2 * piD) - 2 * piD / 3)
      | t <- [0, 0.25 * tMax, 0.5 * tMax, tMax]
      , k <- [0 .. 2] ]
    perRes = maximum
      [ abs (analyticalRadius (t + tR) 1.0 (2 * piD) k
             - analyticalRadius t 1.0 (2 * piD) k)
      | k <- [0 .. 2]
      , t <- [0, 0.137 * tMax, 0.5 * tMax, 0.811 * tMax] ]
    ts    = [ tMax * fromIntegral i / fromIntegral (nPoints - 1)
            | i <- [0 .. nPoints - 1] ]
    cChs  = [ computeChaplygin (analyticalRadius t 1.0 (2 * piD) 0) omega 1.0 0
            | t <- ts ]
    base  = head cChs
    drift = maximum (map (abs . subtract base) cChs)

-- | The V2 integration: RK4 over `rotations` full rotations.
integrateV2 :: Int -> Int -> [Double]
integrateV2 rotations stepsPerPeriod =
  iterateN (rotations * stepsPerPeriod) step (equilateralInitial 1.0)
  where
    omega = lagrangeOmega 1.0 1.0
    dt    = (2 * piD / omega) / fromIntegral stepsPerPeriod
    step st = rk4Step st [1, 1, 1] dt

-- | The V2 tracked trajectory, for the SVG figures.
integrateV2Tracked :: Int -> Int -> [(Double, [Double])]
integrateV2Tracked rotations stepsPerPeriod =
  (0.0, st0) : go 0 st0 []
  where
    st0   = equilateralInitial 1.0
    omega = lagrangeOmega 1.0 1.0
    dt    = (2 * piD / omega) / fromIntegral stepsPerPeriod
    nSteps = rotations * stepsPerPeriod
    every = max (nSteps `div` 400) 1
    go step st acc
      | step == nSteps = reverse acc
      | otherwise =
          let st'  = rk4Step st [1, 1, 1] dt
              acc' = if step `mod` every == 0
                     then (fromIntegral (step + 1) * dt, st') : acc
                     else acc
          in go (step + 1) st' acc'

-- | V2 — rigid rotation + measured vs analytic omega.
checkV2 :: Int -> Int -> Check
checkV2 rotations stepsPerPeriod = Check
  "V2 Lagrange rigid rotation: shape + analytic omega = 3G/(2pi a^2)"
  [ ("shape_drift",          FNum shapeDrift)
  , ("shape_tolerance",      FNum tolRk4)
  , ("omega_analytic",       FNum omega)
  , ("omega_relative_error", FNum omegaRelErr)
  , ("omega_tolerance",      FNum tolOmega)
  , ("params", FMap
      [ ("Gamma", FNum 1.0)
      , ("a", FNum 1.0)
      , ("rotations", FNum (fromIntegral rotations))
      , ("steps_per_period", FNum (fromIntegral stepsPerPeriod))
      , ("dt", FNum dt) ])
  ]
  (shapeDrift <= tolRk4 && omegaRelErr <= tolOmega)
  where
    omega = lagrangeOmega 1.0 1.0
    dt    = (2 * piD / omega) / fromIntegral stepsPerPeriod
    nSteps = rotations * stepsPerPeriod
    st0    = equilateralInitial 1.0
    st1    = integrateV2 rotations stepsPerPeriod
    angStart = atan2 (st0 !! 1) (st0 !! 0)
    angEnd   = atan2 (st1 !! 1) (st1 !! 0)
    -- Unwrap: lift the raw angle difference to the branch closest to the
    -- expected unwrapped angle. Haskell's `round` is half-to-even — the
    -- same banker's rounding CPython uses in the Python twin.
    expectedTotal = omega * fromIntegral nSteps * dt
    raw = angEnd - angStart
    measured = raw + 2 * piD * fromIntegral (round ((expectedTotal - raw) / (2 * piD)) :: Integer)
    omegaRelErr = abs (measured - expectedTotal) / expectedTotal
    (s1, s2, s3) = sideLengths st1
    shapeDrift = maximum [abs (s1 - 1), abs (s2 - 1), abs (s3 - 1)]

-- | V3 — H, P, Q, I conserved along the Lagrange trajectory.
checkV3 :: Int -> Int -> Check
checkV3 rotations stepsPerPeriod = Check
  "V3 vortex integrals: H, P, Q, I conserved (equal Gamma)"
  [ ("relative_drifts", FMap
      [ ("H", FNum dH), ("P", FNum dP), ("Q", FNum dQ), ("I", FNum dI) ])
  , ("worst_drift", FNum worst)
  , ("tolerance", FNum tolRk4)
  , ("params", FMap
      [ ("Gamma", FNum 1.0)
      , ("a", FNum 1.0)
      , ("rotations", FNum (fromIntegral rotations))
      , ("steps_per_period", FNum (fromIntegral stepsPerPeriod)) ])
  ]
  (worst <= tolRk4)
  where
    st0 = equilateralInitial 1.0
    omega = lagrangeOmega 1.0 1.0
    dt  = (2 * piD / omega) / fromIntegral stepsPerPeriod
    inv0 = invariants st0 [1, 1, 1]
    inv1 = invariants (iterateN (rotations * stepsPerPeriod)
                        (\s -> rk4Step s [1, 1, 1] dt) st0) [1, 1, 1]
    drifts = [ abs (b - a) / max (abs a) 1
             | (a, b) <- zip4 inv0 inv1 ]
    zip4 (a, b, c, d) (a', b', c', d') =
      [(a, a'), (b, b'), (c, c'), (d, d')]
    worst = maximum drifts
    dH : dP : dQ : dI : _ = drifts

-- | V4 — integrals conserved for unequal circulations (no symmetry needed).
checkV4 :: Int -> Int -> Check
checkV4 rotations stepsPerPeriod = Check
  "V4 robustness: H, P, Q, I conserved for Gamma = (1, 2, 3)"
  [ ("relative_drifts", FMap
      [ ("H", FNum dH), ("P", FNum dP), ("Q", FNum dQ), ("I", FNum dI) ])
  , ("worst_drift", FNum worst)
  , ("tolerance", FNum tolRk4)
  , ("params", FMap
      [ ("Gamma", FList (map FNum [1, 2, 3]))
      , ("a", FNum 1.0)
      , ("rotations", FNum (fromIntegral rotations))
      , ("steps_per_period", FNum (fromIntegral stepsPerPeriod)) ])
  ]
  (worst <= tolRk4)
  where
    a   = 1.0
    cy  = sqrt 3 / 2 * a
    cx  = (0 + a + 0.5 * a) / 3
    cyy = cy / 3
    st0 = [0 - cx, 0 - cyy, a - cx, 0 - cyy, 0.5 * a - cx, cy - cyy]
    gamma = [1, 2, 3]
    omegaRef = lagrangeOmega 2.0 a
    dt  = (2 * piD / omegaRef) / fromIntegral stepsPerPeriod
    inv0 = invariants st0 gamma
    inv1 = invariants (iterateN (rotations * stepsPerPeriod)
                        (\s -> rk4Step s gamma dt) st0) gamma
    drifts = [ abs (b - a) / max (abs a) 1 | (a, b) <- zip4 inv0 inv1 ]
    zip4 (a, b, c, d) (a', b', c', d') =
      [(a, a'), (b, b'), (c, c'), (d, d')]
    worst = maximum drifts
    dH : dP : dQ : dI : _ = drifts

-- ---------------------------------------------------------------------------
-- The ladder
-- ---------------------------------------------------------------------------

data LadderRun = LadderRun
  { runChecks    :: [Check]
  , runAllPassed :: Bool
  , runWallTime  :: Double
  }

-- | Run V1–V4 with a preset, mirroring the Python ladder's `run`.
runLadder :: Preset -> IO LadderRun
runLadder p = do
  t0 <- cpuSeconds
  let v1 = checkV1 (presetPoints p)
      v2 = checkV2 (presetRotations p) (presetSteps p)
      v3 = checkV3 (presetRotations p) (presetSteps p)
      v4 = checkV4 (max 2 (presetRotations p - 2)) (presetSteps p)
      checks = [v1, v2, v3, v4]
  t1 <- cpuSeconds
  pure (LadderRun checks (all checkPassed checks) (t1 - t0))

foreign import ccall unsafe "clock" c_clock :: IO Int

-- POSIX clock() gives process CPU time in CLOCKS_PER_SEC = 1e6 units.
cpuSeconds :: IO Double
cpuSeconds = fmap (\x -> fromIntegral x / 1e6) c_clock

-- ---------------------------------------------------------------------------
-- The exact-rational dual run over ℚ(√3) — the M3 exactness split
-- ---------------------------------------------------------------------------

-- | ℚ(√3): p + q·√3 with exact Rational coefficients.
data QS = QS Rational Rational

instance Num QS where
  QS a b + QS c d = QS (a + c) (b + d)
  QS a b - QS c d = QS (a - c) (b - d)
  QS a b * QS c d = QS (a * c + 3 * b * d) (a * d + b * c)
  negate (QS a b) = QS (negate a) (negate b)
  abs x = x  -- the dual only needs nonnegative values
  signum (QS a b) = QS (signum a) 0
  fromInteger n = QS (fromInteger n) 0

instance Eq QS where
  -- √3 is irrational: p + q√3 = p' + q'√3 ⟺ p = p' ∧ q = q'
  QS a b == QS c d = a == c && b == d

instance Show QS where
  show (QS a b)
    | b == 0    = showR a
    | a == 0    = "(" ++ showR b ++ ")·√3"
    | otherwise = "(" ++ showR a ++ " + " ++ showR b ++ "·√3)"
    where
      showR r
        | denominator r == 1 = show (numerator r)
        | otherwise = show (numerator r) ++ "/" ++ show (denominator r)

instance Fractional QS where
  -- 1/(p + q√3) = (p − q√3)/(p² − 3q²), exact since p² − 3q² ≠ 0 for
  -- (p,q) ≠ (0,0) (√3 irrational).
  recip (QS a b) = QS (a / den) (negate b / den)
    where den = a * a - 3 * b * b
  fromRational r = QS r 0

-- | One exact anchor: a name, the exact verdict, and a detail line.
data ExactAnchor = ExactAnchor
  { anchorName   :: String
  , anchorPassed :: Bool
  , anchorDetail :: String
  }

-- | The exact-rational dual: the four anchor values of the equilateral
-- reference state (side a = 1, equal circulations) hold BY COMPUTATION:
--
--   v1 = (1/√3, 0), v2 = (−1/(2√3), 1/2), v3 = (−1/(2√3), −1/2)
--   ⇒ sides² = 1 exactly, H = 0, P = 0, Q = 0, I = Γ (Γ = 1 here).
exactAnchors :: [ExactAnchor]
exactAnchors =
  [ ExactAnchor "side squares exactly 1 (all three)"
      (s12sq == one && s23sq == one && s31sq == one)
      ("(Δx)² + (Δy)² for (v1,v2) = " ++ show s12sq)
  , ExactAnchor "P = 0 exactly" (pVal == zero)
      ("Γ·(x1+x2+x3) with x1+x2+x3 = " ++ show (x1 + x2 + x3))
  , ExactAnchor "Q = 0 exactly" (qVal == zero)
      ("Γ·(y1+y2+y3) with y1+y2+y3 = " ++ show (y1 + y2 + y3))
  , ExactAnchor "I = Γ exactly (Γ = 1)" (iVal == one)
      ("Σ‖v‖² = " ++ show normSum)
  , ExactAnchor "H = 0 exactly (distances exactly 1, ln 1 = 0)"
      (s12sq == one && s23sq == one && s31sq == one)
      "H = −(1/2π)·Σ ΓΓ'·ln r_ij with every r_ij = 1"
  ]
  where
    one  = QS 1 0
    zero = QS 0 0
    x1 = QS 0 (1 % 3)        -- 1/√3 = (1/3)·√3
    x2 = QS 0 (negate (1 % 6))  -- −1/(2√3) = −(1/6)·√3
    x3 = x2
    y1 = QS 0 0
    y2 = QS (1 % 2) 0
    y3 = QS (negate (1 % 2)) 0
    d2 ax ay bx by = (ax - bx) * (ax - bx) + (ay - by) * (ay - by)
    s12sq = d2 x1 y1 x2 y2
    s23sq = d2 x2 y2 x3 y3
    s31sq = d2 x3 y3 x1 y1
    pVal = x1 + x2 + x3
    qVal = y1 + y2 + y3
    sqNorm ax ay = ax * ax + ay * ay
    normSum = sqNorm x1 y1 + sqNorm x2 y2 + sqNorm x3 y3
    iVal = normSum

-- ---------------------------------------------------------------------------
-- File writers and SVG plots (dependency-free)
-- ---------------------------------------------------------------------------

writeText :: FilePath -> String -> IO ()
writeText path text = withFile path WriteMode (`hPutStr` text)

writeCsv :: FilePath -> [String] -> [[Double]] -> IO ()
writeCsv path header rows =
  writeText path (intercalate "," header ++ "\n"
                  ++ unlines [ intercalate "," (map jsonFloat row) | row <- rows ])

data SvgSeries = SvgSeries
  { svgLabel  :: String
  , svgPoints :: [(Double, Double)]
  , svgColor  :: String
  }

fmtAxis :: Double -> String
fmtAxis v
  | v == 0                      = "0"
  | abs v < 1e-3 || abs v >= 1e6 =
      let e = floor (logBase 10 (abs v)) :: Int
          m = v / 10 ** fromIntegral e
      in show m ++ "e" ++ show e
  | otherwise                   = show v

xmlEscape :: String -> String
xmlEscape = concatMap esc
  where
    esc '&' = "&amp;"
    esc '<' = "&lt;"
    esc '>' = "&gt;"
    esc c   = [c]

-- | A multi-series line plot as dependency-free vector SVG (sharp at any
-- dpi; the same data re-renders at 600 dpi in the Python laboratory).
svgLinePlot :: FilePath -> String -> String -> String -> [SvgSeries] -> IO ()
svgLinePlot path title xLabel yLabel series = writeText path svg
  where
    (w, h) = (900.0, 560.0) :: (Double, Double)
    (ml, mr, mt, mb) = (72.0, 24.0, 56.0, 64.0) :: (Double, Double, Double, Double)
    pw = w - ml - mr
    ph = h - mt - mb
    pts = concatMap svgPoints series
    xs = map fst pts
    ys = map snd pts
    xmin = if null xs then 0 else minimum xs
    xmax = if null xs then 1 else maximum xs
    ymin0 = if null ys then 0 else minimum ys
    ymax0 = if null ys then 1 else maximum ys
    padY = 0.05 * (ymax0 - ymin0)
    ymin = ymin0 - padY
    ymax = ymax0 + padY
    xmax' = if xmax - xmin < 1e-300 then xmin + 1 else xmax
    ymax' = if ymax - ymin < 1e-300 then ymin + 1 else ymax
    sx x = ml + (x - xmin) / (xmax' - xmin) * pw
    sy y = mt + ph - (y - ymin) / (ymax' - ymin) * ph
    sh :: Double -> String
    sh = show
    gridLines = concat
      [ "<line x1=\"" ++ sh (ml + t * pw) ++ "\" y1=\"" ++ sh mt
        ++ "\" x2=\"" ++ sh (ml + t * pw) ++ "\" y2=\"" ++ sh (mt + ph)
        ++ "\" stroke=\"#e6e8eb\" stroke-width=\"1\"/>"
        ++ "<text x=\"" ++ sh (ml + t * pw) ++ "\" y=\"" ++ sh (mt + ph + 20)
        ++ "\" font-size=\"12\" fill=\"#57606a\" text-anchor=\"middle\">"
        ++ fmtAxis (xmin + t * (xmax' - xmin)) ++ "</text>"
        ++ "<line x1=\"" ++ sh ml ++ "\" y1=\"" ++ sh (mt + ph - t * ph)
        ++ "\" x2=\"" ++ sh (ml + pw) ++ "\" y2=\"" ++ sh (mt + ph - t * ph)
        ++ "\" stroke=\"#e6e8eb\" stroke-width=\"1\"/>"
        ++ "<text x=\"" ++ sh (ml - 8) ++ "\" y=\"" ++ sh (mt + ph - t * ph + 4)
        ++ "\" font-size=\"12\" fill=\"#57606a\" text-anchor=\"end\">"
        ++ fmtAxis (ymin + t * (ymax' - ymin)) ++ "</text>"
      | i <- [0 .. 5], let t = fromIntegral i / 5 ]
    polylines = concat
      [ "<polyline fill=\"none\" stroke=\"" ++ svgColor s
        ++ "\" stroke-width=\"1.8\" stroke-linejoin=\"round\" points=\""
        ++ unwords [ sh (sx x) ++ "," ++ sh (sy y) | (x, y) <- svgPoints s ]
        ++ "\"/>"
      | s <- series ]
    legend = concat
      [ "<line x1=\"" ++ sh (ml + pw - 104) ++ "\" y1=\"" ++ sh ly
        ++ "\" x2=\"" ++ sh (ml + pw - 76) ++ "\" y2=\"" ++ sh ly
        ++ "\" stroke=\"" ++ svgColor s ++ "\" stroke-width=\"2.4\"/>"
        ++ "<text x=\"" ++ sh (ml + pw - 112) ++ "\" y=\"" ++ sh (ly + 4)
        ++ "\" font-size=\"12.5\" fill=\"#1f2328\" text-anchor=\"end\">"
        ++ xmlEscape (svgLabel s) ++ "</text>"
      | (i, s) <- zip [0 ..] series
      , let ly = mt + 16 + fromIntegral i * 22 ]
    svg = concat
      [ "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 900 560\" "
        ++ "font-family=\"'Segoe UI','Helvetica Neue',Arial,sans-serif\">\n"
      , "<rect width=\"900\" height=\"560\" fill=\"#ffffff\"/>\n"
      , "<text x=\"450\" y=\"34\" font-size=\"20\" font-weight=\"600\" "
        ++ "fill=\"#1f2328\" text-anchor=\"middle\">"
        ++ xmlEscape title ++ "</text>\n"
      , gridLines
      , "<line x1=\"" ++ sh ml ++ "\" y1=\"" ++ sh (mt + ph)
        ++ "\" x2=\"" ++ sh (ml + pw) ++ "\" y2=\"" ++ sh (mt + ph)
        ++ "\" stroke=\"#1f2328\" stroke-width=\"1.4\"/>\n"
      , "<line x1=\"" ++ sh ml ++ "\" y1=\"" ++ sh mt
        ++ "\" x2=\"" ++ sh ml ++ "\" y2=\"" ++ sh (mt + ph)
        ++ "\" stroke=\"#1f2328\" stroke-width=\"1.4\"/>\n"
      , polylines
      , "<text x=\"" ++ sh (ml + pw / 2) ++ "\" y=\"" ++ sh (h - 18)
        ++ "\" font-size=\"14\" fill=\"#1f2328\" text-anchor=\"middle\">"
        ++ xmlEscape xLabel ++ "</text>\n"
      , "<text x=\"20\" y=\"" ++ sh (mt + ph / 2)
        ++ "\" font-size=\"14\" fill=\"#1f2328\" text-anchor=\"middle\" "
        ++ "transform=\"rotate(-90 20 " ++ sh (mt + ph / 2) ++ ")\">"
        ++ xmlEscape yLabel ++ "</text>\n"
      , legend
      , "</svg>\n" ]
