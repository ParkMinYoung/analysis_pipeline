# Bioinformatics Pipeline Cost Analysis

생물정보 분석본부 (1팀, 2팀, 3팀) 분석 파이프라인의 AWS Batch 비용 분석 프로젝트

## 프로젝트 개요

이 프로젝트는 생물정보학 분석 파이프라인의 AWS Batch 사용 비용을 계산하고 분석합니다.
팀별로 독립적인 분석이 가능하며, 각 팀의 파이프라인 비용을 개별적으로 추적할 수 있습니다.

### 분석 대상
- **Team 1**: 19개 파이프라인, 338 steps (WGS, WES, DNA Chip, Pangenome, 단백질 분석, 커스텀 분석)
- **Team 2**: 22개 파이프라인, 351 steps (Short RNA, Single Cell RNA, Spatial 등)
- **Team 3**: 8개 파이프라인, 122 steps (Assembly, Microbiome)
- **총 파이프라인**: 49개 (팀별로 상이)
- **플랫폼**: PacBio Revio/Sequel, Illumina NovaSeq/MiSeq, Nanopore PromethION, Axiom/Illumina Microarray

## 디렉토리 구조

```
pipeline_price/
├── data/                           # 팀별 데이터 파일
│   ├── team1/                      # 1팀 데이터
│   │   ├── analysis_raw.csv        # Google Sheets 원본 데이터
│   │   ├── analysis_processed.csv  # 전처리된 데이터
│   │   └── analysis_with_costs.csv # 비용 계산 완료 데이터
│   ├── team2/                      # 2팀 데이터
│   │   └── (동일 구조)
│   └── team3/                      # 3팀 데이터
│       └── (동일 구조)
├── scripts/                        # 공통 분석 스크립트
│   ├── 01_process_data.py          # 데이터 전처리 (팀번호 인자 필수)
│   ├── 02_calculate_aws_costs.py   # AWS 비용 계산 (팀번호 인자 필수)
│   └── 03_analyze_pipelines.py     # 파이프라인 분석 및 리포트 생성 (팀번호 인자 필수)
├── reports/                        # 팀별 리포트
│   ├── team1/                      # 1팀 리포트
│   │   ├── 00_SUMMARY_ALL_PIPELINES.txt
│   │   ├── pipeline_summary.csv
│   │   └── *_report.txt
│   ├── team2/                      # 2팀 리포트
│   │   └── (동일 구조)
│   └── team3/                      # 3팀 리포트
│       └── (동일 구조)
├── docs/                           # 문서
│   └── rule.md                     # 분석 규칙 및 요구사항
└── README.md                       # 이 파일

```

## 분석 프로세스

각 팀별로 독립적으로 분석을 수행합니다. 스크립트 실행 시 팀 번호 (1, 2, 또는 3)를 인자로 전달해야 합니다.

### 0단계: 데이터 준비
- Google Sheets에서 해당 팀의 분석 시트 데이터를 CSV로 다운로드
- `data/team{N}/analysis_raw.csv`로 저장 (예: `data/team3/analysis_raw.csv`)

### 1단계: 데이터 수집 및 전처리
- 병합된 셀 해제 (forward fill)
- 숫자 필드 정리 (쉼표 제거, 타입 변환)

**실행:**
```bash
# 3팀 데이터 처리 예시
python3 scripts/01_process_data.py 3

# 1팀 데이터 처리
python3 scripts/01_process_data.py 1

# 2팀 데이터 처리
python3 scripts/01_process_data.py 2
```

### 2단계: AWS 비용 계산
- **리전**: us-east-1 (N. Virginia)
- **인스턴스 타입**:
  - C6i family (Compute-optimized) - CPU 집약적 작업
  - R6i family (Memory-optimized) - 메모리 집약적 작업
- **과금 방식**:
  - Compute: 인스턴스 시간당 요금 × 실행시간 × 병렬 작업 수
  - Storage: EBS gp3 ($0.08/GB-month)

**실행:**
```bash
# 3팀 비용 계산 예시
python3 scripts/02_calculate_aws_costs.py 3

# 다른 팀도 동일하게
python3 scripts/02_calculate_aws_costs.py 1
python3 scripts/02_calculate_aws_costs.py 2
```

### 3단계: 파이프라인 분석 및 리포트 생성
- 파이프라인별 그룹화
- 비용, 시간, 리소스 요구사항 집계
- 상세 리포트 생성 (`reports/team{N}/` 디렉토리에 저장)

**실행:**
```bash
# 3팀 리포트 생성 예시
python3 scripts/03_analyze_pipelines.py 3

# 다른 팀도 동일하게
python3 scripts/03_analyze_pipelines.py 1
python3 scripts/03_analyze_pipelines.py 2
```

### 전체 프로세스 한번에 실행
```bash
# 특정 팀 (예: 3팀) 전체 분석 실행
python3 scripts/01_process_data.py 3 && \
python3 scripts/02_calculate_aws_costs.py 3 && \
python3 scripts/03_analyze_pipelines.py 3
```

## 주요 결과

### Team 1 비용 요약
- **총 비용**: $20,218.67
- **총 파이프라인**: 19개
- **총 실행 시간**: 384.61 hours
- **주요 직무**: 커스텀 분석 ($19,275.51), Whole Genome Sequencing ($732.98), Pangenome ($154.80)

**Top 5 고비용 파이프라인 (Team 1):**
1. PWAS (Proteome-Wide Association Study): $19,097.80
2. PacBio Revio Human WGS: $257.48
3. Illumina NovaSeq non-Human WGS: $227.64
4. Illumina NovaSeq Human WGS: $216.80
5. Kinics-ICS: $177.71

### Team 2 비용 요약
- **총 비용**: $51,688.29
- **총 파이프라인**: 22개
- **총 실행 시간**: 651.34 hours
- **주요 직무**: Single Cell RNA ($48,288.78), Spatial ($3,114.01), Short RNA Sequencing ($126.92)

**Top 5 고비용 파이프라인 (Team 2):**
1. scRNA_parse_kinnex: $10,445.01
2. scRNA_parse_illumina: $9,812.05
3. scRNA_10x_illumina: $9,376.85
4. scRNA_10x_kinnex: $9,355.57
5. scRNA_scale_illumina: $9,299.31

### Team 3 비용 요약
- **총 비용**: $3,302.47
- **총 파이프라인**: 8개
- **총 실행 시간**: 602.8 hours
- **Assembly 비용**: $1,934.48 (54 steps)
- **Microbiome 비용**: $1,367.99 (68 steps)

**Top 5 고비용 파이프라인 (Team 3):**
1. Large Genome Assembly - All: $1,772.34
2. shotgun metagenome 분석 - Pacbio: $997.53
3. 16S rRNA metagenome - Pacbio: $318.48
4. Small Genome Assembly - Bacteria/Fungi: $84.52
5. Organelle Assembly - CP/MT: $77.62

> 각 팀의 상세 결과는 `reports/team{N}/00_SUMMARY_ALL_PIPELINES.txt`에서 확인할 수 있습니다.

### 가장 비용이 높은 작업 단계

#### Team 1 고비용 단계:
1. **FUSION_wgt** (PWAS): $18,966.59
   - r6i.16xlarge (64 vCPU, 500 GB), 84 hours × 56 parallel tasks
2. **pbmm2_align_wgs** (PacBio WGS): $190.43
   - c6i.16xlarge (32 vCPU, 128 GB), 5 hours × 14 parallel tasks
3. **Correction & Scaffolding** (Pangenome): $140.35
   - r6i.16xlarge (64 vCPU, 500 GB), 8.7 hours × 4 parallel tasks

#### Team 3 고비용 단계:

1. **Flye Assembly** (Shotgun metagenome): $979.77
   - c6i.24xlarge (96 vCPU, 192 GB), 240 hours

2. **Maker Gene Prediction** (Large genome): $871.62
   - r6i.16xlarge (64 vCPU, 512 GB), 36 hours × 6 parallel tasks

3. **Verkko Assembly** (Large genome with Hi-C): $392.48
   - c6i.16xlarge (64 vCPU, 128 GB), 18 hours × 8 parallel tasks

## 리포트 파일 설명

각 팀의 리포트는 `reports/team{N}/` 디렉토리에 생성됩니다.

### `00_SUMMARY_ALL_PIPELINES.txt`
해당 팀의 모든 파이프라인 전체 요약:
- 전체 비용 개요
- 직무별 비용 통계
- 비용순으로 정렬된 파이프라인 목록

### `pipeline_summary.csv`
파이프라인별 요약 데이터 (CSV 형식):
- 파이프라인 정보 (이름, 버전, 플랫폼)
- 리소스 요구사항 (CPU, 메모리, 스토리지)
- 비용 breakdown (compute, storage)

### `*_report.txt`
각 파이프라인의 상세 리포트:
- Overview: 파이프라인 기본 정보
- Resource Requirements: 최대 CPU/메모리/스토리지
- Cost Summary: 총 비용 및 breakdown
- Group별 비용 분석
- Step-by-step 상세 분석

## AWS 가격 정책 (2026년 1월 기준)

### EC2 인스턴스 가격 (us-east-1, On-Demand)

**Compute-Optimized (C6i):**
- c6i.large (2 vCPU, 4 GB): $0.085/hr
- c6i.xlarge (4 vCPU, 8 GB): $0.17/hr
- c6i.2xlarge (8 vCPU, 16 GB): $0.34/hr
- c6i.4xlarge (16 vCPU, 32 GB): $0.68/hr
- c6i.8xlarge (32 vCPU, 64 GB): $1.36/hr
- c6i.12xlarge (48 vCPU, 96 GB): $2.04/hr
- c6i.16xlarge (64 vCPU, 128 GB): $2.72/hr
- c6i.24xlarge (96 vCPU, 192 GB): $4.08/hr

**Memory-Optimized (R6i):**
- r6i.large (2 vCPU, 16 GB): $0.126/hr
- r6i.xlarge (4 vCPU, 32 GB): $0.252/hr
- r6i.2xlarge (8 vCPU, 64 GB): $0.504/hr
- r6i.4xlarge (16 vCPU, 128 GB): $1.008/hr
- r6i.8xlarge (32 vCPU, 256 GB): $2.016/hr
- r6i.12xlarge (48 vCPU, 384 GB): $3.024/hr
- r6i.16xlarge (64 vCPU, 512 GB): $4.032/hr

**EBS Storage (gp3):**
- $0.08 per GB-month = $0.000111 per GB-hour

## 비용 최적화 제안

### 1. Spot Instances 사용
- Spot 인스턴스는 On-Demand 대비 최대 90% 할인
- 중단 가능한 배치 작업에 적합
- 예상 절감액: **~$2,300 (70% 절감)**

### 2. Savings Plans
- 1년 또는 3년 약정으로 최대 72% 할인
- 일관된 사용량이 있는 경우 유리

### 3. 리소스 최적화
- 일부 작업에서 over-provisioned 인스턴스 사용 감지
- 예: 1 CPU만 필요한 작업에 large 인스턴스 사용
- 인스턴스 크기 조정으로 추가 절감 가능

### 4. 스토리지 최적화
- 임시 데이터는 EBS 대신 Instance Store 사용
- 데이터 압축 및 정리로 스토리지 비용 절감

## 데이터 출처

- **원본 데이터**: Google Sheets (3팀_분석)
- **가격 정보**:
  - [AWS EC2 Pricing](https://aws.amazon.com/ec2/pricing/on-demand/)
  - [Economize Cloud Pricing](https://www.economize.cloud/resources/aws/pricing/ec2/)
  - [Instance Comparison Tool](https://instances.vantage.sh/)

## 문의

분석에 대한 질문이나 추가 요청사항이 있으시면 연락 주세요.

---
**최종 업데이트**: 2026-01-08
**분석 완료**: Team 1 (19 pipelines), Team 2 (22 pipelines), Team 3 (8 pipelines)
**총 파이프라인**: 49개
**총 예상 비용**: $75,209.43
**분석 도구**: Python 3.11, pandas, numpy
**AWS 리전**: us-east-1 (N. Virginia)
**지원 팀**: Team 1, Team 2, Team 3
