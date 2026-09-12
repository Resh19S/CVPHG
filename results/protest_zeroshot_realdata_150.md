# Riot/Protest Zero-Shot Results (Real Data, Scaled: 150 Capitol Riot + 50 RLVS Normal)

Zero-shot CLIP (ViT-B-32, openai weights) classification of riot vs. negative-class clips. No fine-tuning. See README.md for scope and limitations.

> Scale-up check on the n=80 result (results/protest_zeroshot_realdata.md): riot class expanded 30->150 real Capitol clips to test whether 0.93 precision / 0.90 recall holds at 5x scale. normal class held at 50 RLVS NonViolence clips (unchanged). RLVS Violence still excluded -- see data/manifest_protest.README.md.

**Clips evaluated:** 200  
**Overall accuracy:** 71.00%

## Per-class precision / recall / F1

| class | precision | recall | f1 | support |
|---|---|---|---|---|
| riot | 0.99 | 0.93 | 0.96 | 150 |
| normal | 1.00 | 0.04 | 0.08 | 50 |
| fighting | 0.00 | 0.00 | 0.00 | 0 |

## Confusion matrix (rows = true label, cols = predicted)

| true \ pred | riot | normal | fighting |
|---|---|---|---|
| riot | 140 | 0 | 10 |
| normal | 2 | 2 | 46 |
| fighting | 0 | 0 | 0 |

## Per-clip predictions

| id | true label | predicted | confidence | correct |
|---|---|---|---|---|
| 0RkqluQmLWCt | riot | fighting | 0.483 | no |
| 0gEXueOMmwi8 | riot | riot | 0.913 | yes |
| 0jaHRfXYTxdk | riot | riot | 0.840 | yes |
| 1Ta9ZdFfiNrZ | riot | riot | 0.930 | yes |
| 1Zvr7Xtfv0Yt | riot | riot | 0.873 | yes |
| 1do91KWUgjXQ | riot | riot | 0.653 | yes |
| 2XwJn0Iqphrc | riot | riot | 0.637 | yes |
| 3PkLpHaNWWeH | riot | riot | 0.904 | yes |
| 3ZXOHhUdKlYd | riot | riot | 0.935 | yes |
| 3vGQyQIMf9H5 | riot | riot | 0.762 | yes |
| 4AquVMy2oe6C | riot | riot | 0.883 | yes |
| 4wIDySD7tKxo | riot | riot | 0.445 | yes |
| 5an2kTUFQs2t | riot | fighting | 0.476 | no |
| 650ut3VxB679 | riot | riot | 0.823 | yes |
| 6FY6c0d8IMjz | riot | riot | 0.956 | yes |
| 6VYEdaOOP3hD | riot | riot | 0.440 | yes |
| 7ImZGTdfdcUk | riot | riot | 0.954 | yes |
| 7WJTCduTUKpl | riot | riot | 0.440 | yes |
| 7fckI1220tbu | riot | riot | 0.929 | yes |
| 7pyX4y0Z2wiy | riot | riot | 0.655 | yes |
| 8fsC1EfPO70k | riot | riot | 0.704 | yes |
| 8ziKp2FKa3Sb | riot | fighting | 0.425 | no |
| 99Z6yIaTknNG | riot | riot | 0.897 | yes |
| 9bJLFfPeZlk8 | riot | riot | 0.937 | yes |
| 9mroY9bM530c | riot | riot | 0.672 | yes |
| ATHRnnmNpayv | riot | riot | 0.515 | yes |
| AYijYnzI0Gbr | riot | riot | 0.602 | yes |
| B7yh3YgnbcFT | riot | riot | 0.910 | yes |
| BnoDFbldwdly | riot | riot | 0.782 | yes |
| BvNA5CiE47yt | riot | riot | 0.895 | yes |
| C4YoY0OUVVNO | riot | riot | 0.959 | yes |
| C6CA3XcXO87g | riot | riot | 0.566 | yes |
| CE7LhOl22vJ9 | riot | riot | 0.822 | yes |
| CKSVgexBTTpn | riot | riot | 0.921 | yes |
| CdZE4mF5ht43 | riot | riot | 0.949 | yes |
| Cg3gG8trkats | riot | fighting | 0.599 | no |
| CgZxY8PDNM9m | riot | riot | 0.937 | yes |
| D1nBUG3Qu3sw | riot | riot | 0.938 | yes |
| DWGQ3kX1t1bF | riot | riot | 0.899 | yes |
| EjkHpFX9ATgp | riot | riot | 0.769 | yes |
| FRPR3VqfBzIF | riot | riot | 0.904 | yes |
| G3QrHQ8hQT2j | riot | riot | 0.941 | yes |
| GNugjVRmu3Bt | riot | riot | 0.651 | yes |
| HS34fpbzqg2b | riot | riot | 0.828 | yes |
| HpFLIM31gIU3 | riot | riot | 0.537 | yes |
| HpQ07PUDmWDk | riot | riot | 0.759 | yes |
| IOqrjPvbQx6s | riot | riot | 0.956 | yes |
| IjCvip4YonXA | riot | riot | 0.901 | yes |
| IlhIaEMwpl6i | riot | riot | 0.861 | yes |
| Iw8f3g3OZ7Ib | riot | riot | 0.895 | yes |
| JFBcTjyx726j | riot | riot | 0.738 | yes |
| JFDVk6DaG1KD | riot | riot | 0.917 | yes |
| JTr7X40BBrhP | riot | riot | 0.883 | yes |
| KAu8c8e4lbDG | riot | fighting | 0.672 | no |
| KDH68TyHUiw5 | riot | riot | 0.550 | yes |
| KMyt1obG9scS | riot | riot | 0.684 | yes |
| KOZwp3W3n68V | riot | riot | 0.946 | yes |
| Kmm034ViQJyl | riot | riot | 0.924 | yes |
| LD5GrQx0MtsI | riot | riot | 0.918 | yes |
| LQN0zyD01D3i | riot | riot | 0.554 | yes |
| LhPiDTMhUSGL | riot | riot | 0.893 | yes |
| LzjH34PY3gv5 | riot | riot | 0.920 | yes |
| M8YHLRH9D7gh | riot | riot | 0.758 | yes |
| MIS1v7mdAmPU | riot | riot | 0.823 | yes |
| NUpAt87SN70T | riot | riot | 0.916 | yes |
| OYFkHMYFMLfZ | riot | riot | 0.927 | yes |
| OgrPDRox3rYY | riot | riot | 0.889 | yes |
| Q7J24BNG2mCD | riot | riot | 0.782 | yes |
| Q7pXj92SdEwH | riot | riot | 0.809 | yes |
| QNPHAGgOFQAp | riot | riot | 0.865 | yes |
| Qef9FWcq57B2 | riot | riot | 0.946 | yes |
| QgPXUnbdhx3q | riot | riot | 0.652 | yes |
| QhHQcvLey9wa | riot | riot | 0.928 | yes |
| QjlS1mXfbokU | riot | riot | 0.902 | yes |
| QsKjvIGPfWKU | riot | riot | 0.906 | yes |
| QuamW4hp4JQw | riot | riot | 0.891 | yes |
| REUyWy1tXI22 | riot | riot | 0.758 | yes |
| TzNP4slvH8hH | riot | riot | 0.717 | yes |
| VXQewijq1iuR | riot | riot | 0.920 | yes |
| WOR0K16Wbi2I | riot | riot | 0.846 | yes |
| bTZISxkK39sH | riot | riot | 0.899 | yes |
| d7W6peU7P7SA | riot | riot | 0.737 | yes |
| jYwFYXnCB8gz | riot | fighting | 0.456 | no |
| mwt1iRwgWYqy | riot | fighting | 0.631 | no |
| nYJeSZQnzWD0 | riot | riot | 0.923 | yes |
| pQf5uxtLtxH5 | riot | riot | 0.939 | yes |
| rgDWmSDLhmhC | riot | riot | 0.907 | yes |
| t4AqEOluEwK2 | riot | riot | 0.519 | yes |
| tXIzFNM5yp9f | riot | riot | 0.795 | yes |
| uWqE9aiqIa5b | riot | riot | 0.942 | yes |
| wsRe9EYoao7V | riot | riot | 0.652 | yes |
| xSgtD3jz8mUZ | riot | riot | 0.938 | yes |
| xf5PcQJRH676 | riot | riot | 0.666 | yes |
| 0261f0TEn46K | riot | riot | 0.738 | yes |
| 0ILtbKNKST48 | riot | riot | 0.628 | yes |
| 0d6xvM4dAiW4 | riot | riot | 0.857 | yes |
| 0lmypbT9naSL | riot | riot | 0.809 | yes |
| 29cZegQUocJb | riot | riot | 0.888 | yes |
| 2DzUC8Jvgx4g | riot | riot | 0.832 | yes |
| 2PBoIh9W74cM | riot | riot | 0.922 | yes |
| 3ViaXA7t2cYc | riot | riot | 0.925 | yes |
| 4nZvifrR6Gb5 | riot | riot | 0.626 | yes |
| 50XYMR09ys3v | riot | riot | 0.903 | yes |
| 55IZysHw38wO | riot | riot | 0.939 | yes |
| 5kf2savkefB7 | riot | riot | 0.893 | yes |
| 67A81y8heYuc | riot | riot | 0.925 | yes |
| 69WACz6SPQg8 | riot | riot | 0.760 | yes |
| 7iB22C7LbbNy | riot | riot | 0.835 | yes |
| 8KdEh2A5hBi1 | riot | riot | 0.957 | yes |
| 8ONiSixYGejX | riot | riot | 0.560 | yes |
| 8cSaamVcsMri | riot | fighting | 0.715 | no |
| 8rCpNjS3g3Ok | riot | riot | 0.825 | yes |
| 8wCMdWEW39Ff | riot | riot | 0.881 | yes |
| 9M4Lnsf790sK | riot | riot | 0.895 | yes |
| 9T1Wgyjt0vKj | riot | riot | 0.931 | yes |
| A1z3oGHrEMaJ | riot | riot | 0.866 | yes |
| AwME4HLA6vtW | riot | riot | 0.836 | yes |
| BFebZCtfR5aF | riot | riot | 0.901 | yes |
| CN67oIug5zAh | riot | riot | 0.598 | yes |
| CPeuy7lOW44J | riot | riot | 0.930 | yes |
| CVJciWvfzVc1 | riot | riot | 0.755 | yes |
| D7gBZ66rFsaJ | riot | riot | 0.850 | yes |
| Dg4C2BcNChXn | riot | riot | 0.813 | yes |
| FH2gzWNmVnUx | riot | riot | 0.907 | yes |
| GW0AjcMLlz1v | riot | riot | 0.609 | yes |
| HITFOk1YWLly | riot | riot | 0.939 | yes |
| HP1SIkO4eErL | riot | riot | 0.865 | yes |
| HhOE7VTVyjIj | riot | riot | 0.937 | yes |
| KWcmmaWP9GGe | riot | fighting | 0.538 | no |
| LAIAfAzBL39U | riot | riot | 0.902 | yes |
| LuLFx5NpoK10 | riot | riot | 0.942 | yes |
| M4qAK9MhEpEF | riot | riot | 0.963 | yes |
| MwV2lwWVgAF3 | riot | riot | 0.852 | yes |
| NZ0P8ssAGysd | riot | riot | 0.874 | yes |
| NxFqzCuhUuWu | riot | riot | 0.932 | yes |
| OVRHonUii72H | riot | riot | 0.874 | yes |
| Oc9WgHNGpAhE | riot | riot | 0.879 | yes |
| OcH04ImVxWii | riot | riot | 0.835 | yes |
| PQdPojnDKG5e | riot | riot | 0.749 | yes |
| Qau1A0qmEkCT | riot | riot | 0.921 | yes |
| Rp3qrB15ypiE | riot | riot | 0.900 | yes |
| S3xTtPUyKMam | riot | riot | 0.820 | yes |
| SHGsCPYkkOFj | riot | riot | 0.498 | yes |
| SytVtt4RWF4v | riot | riot | 0.955 | yes |
| T4Umz6d0SMnc | riot | riot | 0.837 | yes |
| T57zH8SK96yv | riot | riot | 0.874 | yes |
| UC7nTJ2ha9WM | riot | riot | 0.925 | yes |
| W8ltLizECrMG | riot | riot | 0.910 | yes |
| W9d9UvLeBYFu | riot | fighting | 0.614 | no |
| Wvt5X1vEtjgO | riot | riot | 0.882 | yes |
| NonViolence_NV_1 | normal | fighting | 0.862 | no |
| NonViolence_NV_10 | normal | fighting | 0.706 | no |
| NonViolence_NV_11 | normal | riot | 0.443 | no |
| NonViolence_NV_12 | normal | fighting | 0.864 | no |
| NonViolence_NV_13 | normal | fighting | 0.733 | no |
| NonViolence_NV_14 | normal | normal | 0.385 | yes |
| NonViolence_NV_15 | normal | fighting | 0.734 | no |
| NonViolence_NV_16 | normal | fighting | 0.752 | no |
| NonViolence_NV_17 | normal | fighting | 0.691 | no |
| NonViolence_NV_18 | normal | fighting | 0.936 | no |
| NonViolence_NV_19 | normal | fighting | 0.936 | no |
| NonViolence_NV_2 | normal | fighting | 0.606 | no |
| NonViolence_NV_20 | normal | fighting | 0.891 | no |
| NonViolence_NV_21 | normal | fighting | 0.894 | no |
| NonViolence_NV_22 | normal | fighting | 0.681 | no |
| NonViolence_NV_23 | normal | fighting | 0.684 | no |
| NonViolence_NV_24 | normal | fighting | 0.609 | no |
| NonViolence_NV_25 | normal | fighting | 0.838 | no |
| NonViolence_NV_26 | normal | fighting | 0.838 | no |
| NonViolence_NV_27 | normal | fighting | 0.891 | no |
| NonViolence_NV_28 | normal | fighting | 0.734 | no |
| NonViolence_NV_29 | normal | fighting | 0.947 | no |
| NonViolence_NV_3 | normal | fighting | 0.785 | no |
| NonViolence_NV_30 | normal | fighting | 0.673 | no |
| NonViolence_NV_31 | normal | fighting | 0.770 | no |
| NonViolence_NV_32 | normal | fighting | 0.775 | no |
| NonViolence_NV_33 | normal | fighting | 0.578 | no |
| NonViolence_NV_34 | normal | fighting | 0.772 | no |
| NonViolence_NV_35 | normal | fighting | 0.797 | no |
| NonViolence_NV_36 | normal | fighting | 0.931 | no |
| NonViolence_NV_37 | normal | fighting | 0.680 | no |
| NonViolence_NV_38 | normal | fighting | 0.911 | no |
| NonViolence_NV_39 | normal | fighting | 0.665 | no |
| NonViolence_NV_4 | normal | fighting | 0.636 | no |
| NonViolence_NV_40 | normal | fighting | 0.632 | no |
| NonViolence_NV_41 | normal | fighting | 0.515 | no |
| NonViolence_NV_42 | normal | fighting | 0.890 | no |
| NonViolence_NV_43 | normal | normal | 0.427 | yes |
| NonViolence_NV_44 | normal | fighting | 0.645 | no |
| NonViolence_NV_45 | normal | fighting | 0.635 | no |
| NonViolence_NV_46 | normal | fighting | 0.965 | no |
| NonViolence_NV_47 | normal | fighting | 0.809 | no |
| NonViolence_NV_48 | normal | fighting | 0.569 | no |
| NonViolence_NV_49 | normal | fighting | 0.649 | no |
| NonViolence_NV_5 | normal | fighting | 0.636 | no |
| NonViolence_NV_50 | normal | fighting | 0.672 | no |
| NonViolence_NV_6 | normal | fighting | 0.562 | no |
| NonViolence_NV_7 | normal | riot | 0.633 | no |
| NonViolence_NV_8 | normal | fighting | 0.549 | no |
| NonViolence_NV_9 | normal | fighting | 0.679 | no |