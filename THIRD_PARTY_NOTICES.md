# Third-party notices

이 문서는 외부 구성요소와 프로젝트 자료의 출처·이용 조건을 구분합니다. 저장소 공개는 팀 소유 코드 전체에 오픈소스 라이선스를 부여하는 행위가 아닙니다. 외부 구성요소에는 각 권리자의 조건이 우선 적용됩니다.

팀원들의 공개 동의를 받아 수업·포트폴리오 목적으로 정리했습니다. 실제 사용자 데이터, DB 내용, 비밀키, 개인 음성, 서비스 계정과 개인정보는 공개 대상에서 제외합니다. 문서에 등장하는 서비스명은 기술 설명용이며 제휴·보증을 뜻하지 않습니다.

## 데이터셋
- Caltech-UCSD Birds-200-2011 (CUB-200-2011): [공식 배포처](https://www.vision.caltech.edu/datasets/cub_200_2011/).
- 인용: Wah, C.; Branson, S.; Welinder, P.; Perona, P.; Belongie, S. (2011), The Caltech-UCSD Birds-200-2011 Dataset, California Institute of Technology, CNS-TR-2011-001.
- 배포처는 사진의 저작권을 소유하지 않으며 비상업적 연구·교육 용도로 제한한다고 안내합니다. 본 저장소에는 데이터셋 사진·주석·원본 발표 캡처를 포함하지 않습니다.

## 모델
- PyTorch / TorchVision: [공식 저장소](https://github.com/pytorch/vision), TorchVision BSD-3-Clause. ResNet18과 ConvNeXt는 설치된 TorchVision에서 참조합니다.
- 사전학습 가중치는 저장소에 포함하지 않습니다. [TorchVision 고지](https://docs.pytorch.org/vision/main/models)에 따라 가중치와 학습 데이터에 별도 이용 조건이 있을 수 있으며 사용자가 용도 적합성을 확인해야 합니다.

## 직접 제작한 시각자료
- `docs/hero.svg`: 프로젝트 설명 배너.
- `docs/performance-comparison.svg`: `results/summary.csv` 수치를 다시 그린 결과 그래프.
- `docs/gradcam-concept.svg`: 직접 그린 원리 설명도. 실제 Grad-CAM 결과나 데이터셋 사진이 아닙니다.
