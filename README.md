# FIR Filter Window Comparison for Noise Reduction in digital signals

## Project Overview
This project compares different window-based FIR filters for noise reduction in digital signals. Five window functions are tested: Rectangular, Hamming, Hanning, Blackman, and Kaiser.

## Results Summary
- Best Performance: Kaiser window (β=14) with 6.61 dB SNR improvement
- least Performance: Rectangular window with 6.28 dB SNR improvement

## Parameters Used
| Parameter          | Value   |
| Sampling Frequency | 1000 Hz |
| Filter Order       | 51      |
| Cutoff Frequency   | 100 Hz  |
| Kaiser Beta        | 14      |

## Results Table
| Window      | SNR Before | SNR After | Improvement | RMSE   |
| Rectangular | 3.20       | 9.48      | 6.28        | 0.2375 |
| Hamming     | 3.20       | 9.62      | 6.43        | 0.2335 |
| Hanning     | 3.20       | 9.63      | 6.43        | 0.2334 |
| Blackman    | 3.20       | 9.72      | 6.52        | 0.2310 |
| Kaiser(β=14)| 3.20       | 9.81      | 6.61        | 0.2287 |

## Performance Ranking
Kaiser > Blackman > Hanning ≈ Hamming > Rectangular

## How to Run
1. Install required libraries:
   pip install numpy scipy matplotlib
2. Run the code:
   python main.py

## Files in this Repository
- main.py          - Python code for filter implementation
- report.pdf       - Complete project report
- requirements.txt - Required Python libraries
- results         - All generated figures (4 images)

## Author
Anil Kumar

## Course
EC208-Digital Signal Processing

## Date
07th,April 2026