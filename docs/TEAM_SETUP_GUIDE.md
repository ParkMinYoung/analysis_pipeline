# 팀별 분석 설정 가이드

이 가이드는 Team 1과 Team 2가 파이프라인 비용 분석을 시작하기 위한 단계별 지침을 제공합니다.

## 사전 요구사항

1. Google Sheets에 팀별 분석 데이터가 준비되어 있어야 합니다
2. Python 3.x 설치 확인: `python3 --version`
3. 필요한 라이브러리 설치: `pip install pandas numpy`

## 1단계: Google Sheets 데이터 준비

### 필수 컬럼 구조

Google Sheets에는 다음 컬럼들이 포함되어야 합니다:

| 컬럼명 | 설명 | 예시 |
|--------|------|------|
| idx | 순번 | 1, 2, 3, ... |
| 직무(업무명) | 직무 분류 | Assembly, Microbiome |
| 업무세부내역 | 세부 업무 내용 | Large Genome Assembly (Human, Animal, Plant) |
| Analysis_name | 분석 이름 (선택) | Large Genome Assembly - All |
| Platfom | 플랫폼 정보 | PacBio Revio, Illumina NovaSeq |
| Pipeline Name | 파이프라인 이름 | inhouse |
| Pipeline Version | 파이프라인 버전 | 1.0.0 |
| Group | 그룹 이름 | DE_NOVO_ASSEMBLY |
| Step | 단계 이름 | ASSEMBLY (long read + hi-c) |
| tools | 사용 도구 | hifiasm |
| version | 도구 버전 | 0.16.1 |
| CPUs | CPU 수 | 64 |
| MEM(G) | 메모리 (GB) | 97 |
| TIME(hr) | 실행 시간 (시간) | 14 |
| nTask(병렬) | 병렬 작업 수 | 1 |
| SIZE(MB) | 스토리지 (MB) | 18000 |
| USER | 담당자 | 홍길동 |
| 비고 | 비고 | GenomeSize 3Gb 기준 |

### 중요 사항

1. **병합된 셀**: 같은 파이프라인 내에서 반복되는 값(직무, 업무세부내역, Pipeline Name 등)은 병합된 상태로 두셔도 됩니다. 스크립트가 자동으로 처리합니다.

2. **숫자 형식**: 숫자 필드에 쉼표가 포함되어 있어도 괜찮습니다 (예: 1,000). 스크립트가 자동으로 제거합니다.

3. **빈 값**: 데이터가 없는 경우 빈 칸 또는 '-'로 표시하면 됩니다.

## 2단계: CSV 파일 다운로드

1. Google Sheets에서 파일 → 다운로드 → 쉼표로 구분된 값(.csv, 현재 시트)
2. 파일명을 `analysis_raw.csv`로 변경
3. 프로젝트의 해당 팀 폴더에 저장:
   ```bash
   # Team 1의 경우
   cp ~/Downloads/analysis_raw.csv /path/to/pipeline_price/data/team1/

   # Team 2의 경우
   cp ~/Downloads/analysis_raw.csv /path/to/pipeline_price/data/team2/
   ```

## 3단계: 분석 실행

### Team 1 분석 실행

```bash
cd /path/to/pipeline_price

# 1단계: 데이터 전처리
python3 scripts/01_process_data.py 1

# 2단계: 비용 계산
python3 scripts/02_calculate_aws_costs.py 1

# 3단계: 리포트 생성
python3 scripts/03_analyze_pipelines.py 1
```

### Team 2 분석 실행

```bash
cd /path/to/pipeline_price

# 1단계: 데이터 전처리
python3 scripts/01_process_data.py 2

# 2단계: 비용 계산
python3 scripts/02_calculate_aws_costs.py 2

# 3단계: 리포트 생성
python3 scripts/03_analyze_pipelines.py 2
```

### 한 번에 전체 실행

```bash
# Team 1
python3 scripts/01_process_data.py 1 && \
python3 scripts/02_calculate_aws_costs.py 1 && \
python3 scripts/03_analyze_pipelines.py 1

# Team 2
python3 scripts/01_process_data.py 2 && \
python3 scripts/02_calculate_aws_costs.py 2 && \
python3 scripts/03_analyze_pipelines.py 2
```

## 4단계: 결과 확인

### 생성된 파일 위치

#### Team 1
```
data/team1/
├── analysis_raw.csv          # 원본 데이터
├── analysis_processed.csv    # 전처리된 데이터
└── analysis_with_costs.csv   # 비용 계산 완료 데이터

reports/team1/
├── 00_SUMMARY_ALL_PIPELINES.txt  # 전체 요약
├── pipeline_summary.csv           # 파이프라인별 요약 (CSV)
└── *_report.txt                   # 각 파이프라인별 상세 리포트
```

#### Team 2
```
data/team2/
└── (동일 구조)

reports/team2/
└── (동일 구조)
```

### 주요 리포트 내용

1. **00_SUMMARY_ALL_PIPELINES.txt**
   - 팀 전체 파이프라인 비용 요약
   - 직무별 비용 통계
   - 비용순 파이프라인 목록

2. **pipeline_summary.csv**
   - 파이프라인별 요약 데이터 (엑셀에서 열기 가능)
   - 비용, 시간, 리소스 정보

3. **개별 파이프라인 리포트 (*_report.txt)**
   - 파이프라인 상세 정보
   - Group별 비용 분석
   - Step-by-step 비용 breakdown

## 5단계: 결과 해석

### 비용 계산 방식

```
총 비용 = Compute 비용 + Storage 비용

Compute 비용 = 시간당 인스턴스 요금 × 실행시간 × 병렬 작업 수
Storage 비용 = 스토리지 용량(GB) × 시간 × $0.000111/GB-hour
```

### EC2 인스턴스 자동 선택

스크립트는 각 단계의 CPU와 메모리 요구사항에 맞는 가장 비용 효율적인 EC2 인스턴스를 자동으로 선택합니다:

- **CPU 집약적**: C6i family (Compute-optimized)
- **메모리 집약적**: R6i family (Memory-optimized)

### 비용 최적화 팁

1. **Spot Instances 고려**: On-Demand 대비 최대 90% 절감
2. **병렬 작업 수 최적화**: 불필요한 병렬 작업 제거
3. **리소스 right-sizing**: 필요 이상의 CPU/메모리 할당 방지
4. **임시 데이터 관리**: Instance Store 활용

## 문제 해결

### 자주 발생하는 오류

#### 1. "File not found" 오류
```bash
# 해결: data/team{N} 폴더에 analysis_raw.csv 파일이 있는지 확인
ls -la data/team1/analysis_raw.csv
```

#### 2. "No module named 'pandas'" 오류
```bash
# 해결: 필요한 라이브러리 설치
pip install pandas numpy
```

#### 3. 숫자 필드 파싱 오류
- Google Sheets의 숫자 필드에 특수 문자나 텍스트가 섞여있지 않은지 확인
- 쉼표, 빈 칸, '-' 등은 스크립트가 자동 처리하므로 괜찮습니다

#### 4. 병합 셀 관련 문제
- 병합된 셀은 스크립트가 자동으로 forward fill 처리합니다
- CSV로 다운로드 시 병합 정보가 유지되는지 확인하세요

## Team 3 예시 참고

Team 3의 분석 결과를 참고하시면 도움이 됩니다:
- `reports/team3/00_SUMMARY_ALL_PIPELINES.txt` - 전체 요약 예시
- `reports/team3/pipeline_summary.csv` - CSV 형식 예시
- `reports/team3/*_report.txt` - 상세 리포트 예시

## 추가 지원

분석 중 문제가 발생하거나 질문이 있으시면:
1. `docs/rule.md` 파일의 분석 규칙 확인
2. README.md 파일의 상세 설명 참고
3. 프로젝트 관리자에게 문의

---
**작성일**: 2026-01-06
**버전**: 1.0
**대상**: Team 1, Team 2
