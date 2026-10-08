-- SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
-- SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
-- ===========================================================================
-- TRIVORTEX Haskell guard — the CI-callable checks of the M3 acceptance
-- criteria: pinned reference values (recomputed from the closed form —
-- pinned, not assumed), the quick ladder verdicts, and the exact ℚ(√3)
-- anchor identities.
-- ===========================================================================
module Main (main) where

import System.Exit
import System.IO

import Trivortex.Verify

pi' :: Double
pi' = piD

checkClose :: String -> Double -> Double -> Double -> IO Bool
checkClose what got expected rel = do
  let err = abs (got - expected) / max (abs expected) 1.0
  if err <= rel
    then do putStrLn ("  ok " ++ what ++ " = " ++ show got); pure True
    else do putStrLn ("FAIL " ++ what ++ ": got " ++ show got
                      ++ ", expected " ++ show expected
                      ++ " (rel err " ++ show err ++ ")")
            pure False

checkTrue :: String -> Bool -> IO Bool
checkTrue what cond
  | cond      = do putStrLn ("  ok " ++ what); pure True
  | otherwise = do putStrLn ("FAIL " ++ what); pure False

main :: IO ()
main = do
  hSetEncoding stdout utf8
  putStrLn "TRIVORTEX Haskell guard — pinned reference values"

  -- Theorem 3.1 analytic pins (mirroring test_trivortex.py)
  r1 <- checkClose "omega(C=1, T=2pi)" (analyticalFrequency 1.0 (2 * pi'))
                    1.3748022274393588 1e-12
  r2 <- checkClose "eps(C=1)" (analyticalAmplitude 1.0)
                    (1 / (exp (1 / pi') - 1)) 1e-15
  r3 <- checkTrue "eps guard (C<=0.01) returns 1" (analyticalAmplitude 0.005 == 1.0)

  let omegaRef = analyticalFrequency 1.0 (2 * pi')
      tR       = 2 * pi' / omegaRef
  r4 <- pure (all (\k ->
            abs (analyticalRadius (1.234 + tR) 1.0 (2 * pi') k
                 - analyticalRadius 1.234 1.0 (2 * pi') k) <= 1e-12) [0 .. 2])
  r4' <- checkTrue "closed-form periodicity" r4

  r5 <- checkClose "chaplygin shape" (computeChaplygin 0.5 2.0 1.0 0.0)
                    (0.5 * 0.5 * 2.0 - 1.0 * 0.5) 1e-15
  r6 <- checkClose "omega_Lagrange(1,1)" (lagrangeOmega 1.0 1.0)
                    (3 / (2 * pi')) 1e-15
  r7 <- checkClose "omega_Lagrange(2,3)" (lagrangeOmega 2.0 3.0)
                    (6 / (2 * pi' * 9)) 1e-15

  let st0 = equilateralInitial 1.0
      (s1, s2, s3) = sideLengths st0
  r8 <- checkTrue "equilateral sides"
         (abs (s1 - 1) <= 1e-14 && abs (s2 - 1) <= 1e-14 && abs (s3 - 1) <= 1e-14)

  let d = vortexRhs [1, 0, -1, 0] [1, 1]
  r9  <- checkTrue "pair antisymmetry dx"
          (abs (d !! 0) <= 1e-15 && abs (d !! 2) <= 1e-15)
  r10 <- checkClose "pair dy0" (d !! 1) (0.5 / (2 * pi')) 1e-14
  r11 <- checkClose "pair dy1" (d !! 3) (negate (0.5 / (2 * pi'))) 1e-14

  -- the quick ladder: verdicts inside the registered bands
  run <- runLadder presetQuick
  let checks = runChecks run
      fieldOf i nm = case lookup nm (checkFields (checks !! i)) of
                       Just (FNum x) -> x
                       _             -> 0 / 0
  r12 <- checkTrue "quick ladder all passed" (runAllPassed run)
  r13 <- checkClose "V2 omega_analytic pin" (fieldOf 1 "omega_analytic")
                    0.477464829275686 1e-12
  r14 <- checkTrue "V1 separation band"
          (fieldOf 0 "angular_separation_error" <= 1e-12)
  r15 <- checkTrue "V2 shape band" (fieldOf 1 "shape_drift" <= 1e-10)
  r16 <- checkTrue "V2 omega band" (fieldOf 1 "omega_relative_error" <= 1e-6)
  r17 <- checkTrue "V3 drift band" (fieldOf 2 "worst_drift" <= 1e-10)
  r18 <- checkTrue "V4 drift band" (fieldOf 3 "worst_drift" <= 1e-10)

  -- the exact ℚ(√3) anchors: identities that hold BY COMPUTATION
  r19 <- checkTrue "exact anchors (5 identities)" (all anchorPassed exactAnchors)

  -- JSON serialization smoke
  let json = reportToJson "trivortex-verification-haskell" "quick"
                          "1970-01-01T00:00:00+00:00" checks (runWallTime run)
  r20 <- checkTrue "json contains suite" (take 12 (drop 3 json) == "suite" || contains "\"suite\"" json)
  r21 <- checkTrue "json contains all_passed" (contains "\"all_passed\"" json)

  let results = [r1, r2, r3, r4', r5, r6, r7, r8, r9, r10, r11,
                 r12, r13, r14, r15, r16, r17, r18, r19, r20, r21]
  if and results
    then putStrLn "ALL HASKELL GUARD TESTS PASSED"
    else putStrLn (show (length (filter not results)) ++ " GUARD TEST(S) FAILED")
         >> exitFailure
  where
    contains needle hay = any (needle `prefixOf`) (suffixes hay)
    prefixOf p s = p == take (length p) s
    suffixes []     = [[]]
    suffixes s@(_:t) = s : suffixes t
