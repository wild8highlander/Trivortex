-- SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
-- SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
-- ===========================================================================
-- TRIVORTEX — VERIFICATION LABORATORY (Haskell, interactive)
-- ===========================================================================
-- The interactive laboratory around the Haskell dual ladder (milestone M3):
--   * run the V1–V4 ladder (presets quick / default / full);
--   * the exact-rational dual: the five ℚ(√3) anchor identities;
--   * a convergence study (measured omega error vs integration grid);
--   * SVG plot export (vector figures — sharp at any dpi; the same data
--     re-renders at 600 dpi raster in the Python laboratory);
--   * CSV data export and a JSON protocol per run;
--   * a bilingual interface (English / Русский).
--
-- Author: Isaev Iskhak Khamzatovich (repository owner)
-- Year: 2026
-- ===========================================================================

module Main (main) where

import System.IO

import Trivortex.Verify

suiteName :: String
suiteName = "trivortex-verification-haskell"

data Lang = En | Ru deriving (Eq, Show)

tr :: Lang -> String -> String -> String
tr En en _  = en
tr Ru _  ru = ru

outDirDefault :: FilePath
outDirDefault = "verification/outputs/haskell"

-- ---------------------------------------------------------------------------
-- Menu
-- ---------------------------------------------------------------------------

main :: IO ()
main = do
  hSetEncoding stdout utf8
  hSetBuffering stdout LineBuffering
  putStrLn ""
  putStrLn "╔══════════════════════════════════════════════════════════════════╗"
  putStrLn "║  TRIVORTEX — Verification Laboratory (Haskell dual ladder, M3)   ║"
  putStrLn "║  TRIVORTEX — Лаборатория верификации (Haskell двойник, M3)       ║"
  putStrLn "╚══════════════════════════════════════════════════════════════════╝"
  langStr <- prompt "Language / Язык: [1] English  [2] Русский  > "
  let lang = if langStr == "2" then Ru else En
  loop lang
  where
    loop lang = do
      putStrLn ""
      putStrLn (tr lang "MAIN MENU" "ГЛАВНОЕ МЕНЮ")
      mapM_ (putStrLn . tr lang)
        [ " 1) Run the verification ladder V1–V4 (preset)"
        , " 2) The exact-rational dual: ℚ(√3) anchor identities"
        , " 3) Analysis: convergence study (omega error vs grid)"
        , " 4) Plots: export SVG figures"
        , " 5) Export CSV data"
        , " 0) Exit"
        ]
      pick <- prompt (tr lang "choice> " "выбор> ")
      case pick of
        "1" -> do
          pn <- prompt (tr lang "Preset [quick/default/full] (default: default): "
                              "Пресет [quick/default/full] (по умолчанию: default): ")
          let name = if null pn then "default" else pn
          case findPreset name of
            Nothing -> putStrLn (tr lang "unknown preset" "неизвестный пресет") >> loop lang
            Just p  -> do
              run <- runLadder p
              date <- utcNowIso
              stamp <- utcStamp
              printChecks lang (runChecks run)
              let path = outDirDefault ++ "/trivortex_verify_" ++ name ++ "_" ++ stamp ++ ".json"
              writeText path (reportToJson suiteName name date (runChecks run) (runWallTime run))
              putStrLn (tr lang "JSON protocol saved to " "JSON-протокол сохранён в " ++ path)
              loop lang
        "2" -> do
          putStrLn (tr lang "Exact-rational dual run over ℚ(√3):"
                            "Точный рациональный прогон над ℚ(√3):")
          mapM_ (\a -> putStrLn ("  [" ++ (if anchorPassed a then "EXACT ✓" else "MISMATCH")
                                 ++ "] " ++ anchorName a ++ " — " ++ anchorDetail a))
                exactAnchors
          if all anchorPassed exactAnchors
            then putStrLn (tr lang "  → all five anchors hold by computation."
                                  "  → все пять якорей выполняются вычислением.")
            else putStrLn (tr lang "  → MISMATCH — investigate before proceeding."
                                  "  → РАСХОЖДЕНИЕ — разберитесь до продолжения.")
          loop lang
        "3" -> do
          putStrLn (tr lang "steps/period   omega_rel_err     shape_drift"
                            "шагов/период    отн.ошибка omega  дрейф формы")
          mapM_ (\spp -> do
                  let c = checkV2 2 spp
                      FNum err = case lookup "omega_relative_error" (checkFields c) of
                                  Just v  -> v
                                  Nothing -> FNum (0/0)
                      FNum shp = case lookup "shape_drift" (checkFields c) of
                                  Just v  -> v
                                  Nothing -> FNum (0/0)
                  putStrLn ("  " ++ pad 13 (show spp) ++ "   "
                            ++ pad 13 (show err) ++ "   " ++ show shp)
                ) [250, 500, 1000, 2000, 4000, 8000]
          loop lang
        "4" -> do
          exportPlots lang
          putStrLn (tr lang "SVG plots saved to verification/outputs/haskell/plots"
                            "SVG-графики сохранены в verification/outputs/haskell/plots")
          loop lang
        "5" -> do
          exportCsv
          putStrLn (tr lang "CSV data saved to verification/outputs/haskell/data"
                            "CSV-данные сохранены в verification/outputs/haskell/data")
          loop lang
        "0" -> putStrLn (tr lang "Goodbye — and keep every number bound to a run."
                                 "До встречи — и держите каждое число привязанным к запуску.")
        _   -> putStrLn (tr lang "Invalid choice, try again."
                                 "Неверный пункт, попробуйте ещё раз.") >> loop lang

pad :: Int -> String -> String
pad n s = s ++ replicate (n - length s) ' '

prompt :: String -> IO String
prompt text = do
  putStr text
  hFlush stdout
  line <- getLine
  pure (trim line)
  where
    trim = f . f
    f = reverse . dropWhile (== ' ')

printChecks :: Lang -> [Check] -> IO ()
printChecks lang checks = do
  putStrLn "════════════════════════════════════════════════════════════════"
  mapM_ printCheck checks
  let nPass = length (filter checkPassed checks)
  putStrLn "────────────────────────────────────────────────────────────────"
  putStrLn ("  " ++ tr lang "RESULT" "ИТОГ" ++ ": " ++ show nPass ++ "/"
            ++ show (length checks) ++ " "
            ++ tr lang "checks passed" "проверок пройдено")
  putStrLn "════════════════════════════════════════════════════════════════"
  where
    printCheck c = do
      putStrLn ("[" ++ (if checkPassed c then tr lang "PASS" "ПРОЙДЕНО"
                                            else tr lang "FAIL" "ПРОВАЛ")
                ++ "] " ++ checkName c)
      mapM_ printField (checkFields c)
    printField (k, FNum x)    = putStrLn ("    " ++ k ++ " = " ++ show x)
    printField (k, FStr s)    = putStrLn ("    " ++ k ++ " = " ++ s)
    printField (k, FBool b)   = putStrLn ("    " ++ k ++ " = " ++ show b)
    printField (k, FMap ms)   = do
      putStrLn ("    " ++ k ++ ":")
      mapM_ (\(kk, FNum v) -> putStrLn ("      " ++ kk ++ " = " ++ show v)) ms
    printField (_, FList _)   = pure ()

-- ---------------------------------------------------------------------------
-- Plots and data
-- ---------------------------------------------------------------------------

exportPlots :: Lang -> IO ()
exportPlots _lang = do
  -- fig 1: r_k(t) of Theorem 3.1, k = 0,1,2 over two modulation periods
  let omega = analyticalFrequency 1.0 (2 * piD)
      tR    = 2 * piD / omega
      n     = 600
      tGrid = [ fromIntegral i / fromIntegral n * 2 * tR | i <- [0 .. n] ]
      fig1  = [ SvgSeries ("k = " ++ show k)
                           [ (t, analyticalRadius t 1.0 (2 * piD) k) | t <- tGrid ]
                           (colorOf k)
              | k <- [0 .. 2] ]
  svgLinePlot "verification/outputs/haskell/plots/fig1_closed_form.svg"
    "Theorem 3.1 closed form: r_k(t) over two modulation periods" "t" "r_k(t)" fig1

  -- fig 2: the Section-6 Chaplygin diagnostic over [0, 100T]
  let tMax = 100 * 2 * piD
      m    = 1000
      diag = [ (t, computeChaplygin (analyticalRadius t 1.0 (2 * piD) 0) omega 1.0 0)
             | i <- [0 .. m - 1], let t = fromIntegral i / fromIntegral (m - 1) * tMax ]
  svgLinePlot "verification/outputs/haskell/plots/fig2_chaplygin_diagnostic.svg"
    "Section-6 diagnostic: C_Ch(t) over [0, 100T]" "t" "C_Ch(t)"
    [SvgSeries "C_Ch(t)" diag "#d29922"]

  -- fig 3: the tracked Lagrange rigid rotation
  let traj  = integrateV2Tracked 2 2000
      fig3  = [ SvgSeries ("vortex " ++ show v)
                          [ (t, s !! (2 * v)) | (t, s) <- traj ] (colorOf v)
                | v <- [0 .. 2] ]
  svgLinePlot "verification/outputs/haskell/plots/fig3_lagrange_trajectory.svg"
    "V2: rigid rotation, omega = 3G/(2 pi a^2)" "x" "y" fig3

  -- fig 4: convergence
  let conv = [ (fromIntegral spp, errOf spp) | spp <- [250, 500, 1000, 2000, 4000, 8000] ]
      errOf spp = case lookup "omega_relative_error" (checkFields (checkV2 2 spp)) of
                    Just (FNum e) -> e
                    _             -> 0
  svgLinePlot "verification/outputs/haskell/plots/fig4_convergence.svg"
    "V2 convergence: omega relative error vs steps/period" "steps per period"
    "omega relative error" [SvgSeries "omega_rel_err" conv "#f85149"]

  -- fig 5: the V4 unequal-circulation trajectory (tracked)
  let a  = 1.0 :: Double
      cy = sqrt 3 / 2 * a
      cx = (a + 0.5 * a) / 3
      cyy = cy / 3
      st0 = [0 - cx, 0 - cyy, a - cx, 0 - cyy, 0.5 * a - cx, cy - cyy]
      g4  = [1, 2, 3] :: [Double]
      omegaRef = lagrangeOmega 2.0 a
      dt4 = (2 * piD / omegaRef) / 4000
      n4  = 3 * 4000
      every4 = max (n4 `div` 400) 1
      go4 k st acc
        | k == n4   = reverse acc
        | otherwise =
            let st'  = rk4Step st g4 dt4
                acc' = if k `mod` every4 == 0
                       then (fromIntegral (k + 1) * dt4, st') : acc
                       else acc
            in go4 (k + 1) st' acc'
      traj4 = (0.0, st0) : go4 0 st0 []
      fig5 = [ SvgSeries ("Gamma_" ++ show (v + 1))
                         [ (t, s !! (2 * v)) | (t, s) <- traj4 ] (colorOf v)
             | v <- [0 .. 2] ]
  svgLinePlot "verification/outputs/haskell/plots/fig5_v4_unequal.svg"
    "V4: unequal circulations Gamma = (1, 2, 3), generic triangle" "x" "y" fig5

colorOf :: Int -> String
colorOf 0 = "#1f6feb"
colorOf 1 = "#d29922"
colorOf 2 = "#3fb950"
colorOf _ = "#f85149"

exportCsv :: IO ()
exportCsv = do
  let traj = integrateV2Tracked 2 2000
  writeCsv "verification/outputs/haskell/data/v2_trajectory.csv"
    ["t", "x0", "y0", "x1", "y1", "x2", "y2"]
    [ t : s | (t, s) <- traj ]
  let omega = analyticalFrequency 1.0 (2 * piD)
      tMax  = 100 * 2 * piD
  writeCsv "verification/outputs/haskell/data/v1_chaplygin_diagnostic.csv"
    ["t", "r0", "C_Ch"]
    [ [t, analyticalRadius t 1.0 (2 * piD) 0,
       computeChaplygin (analyticalRadius t 1.0 (2 * piD) 0) omega 1.0 0]
    | i <- [0 .. 999 :: Int]
    , let t = fromIntegral i / 999 * tMax ]
