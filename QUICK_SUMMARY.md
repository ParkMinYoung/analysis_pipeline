# 생물정보 분석 파이프라인 비용 분석 - 빠른 요약

## 목차 (Table of Contents)

1. [전체 요약 (Team 2 + Team 3)](#전체-요약)
2. [Team 2 분석 (22 pipelines)](#team-2-분석)
3. [Team 3 분석 (8 pipelines)](#team-3-분석)
4. [주요 파일 위치](#주요-파일-위치)

---

## 전체 요약

### 📊 양 팀 통합 현황

| 항목 | Team 2 | Team 3 | 합계 |
|------|--------|--------|------|
| **파이프라인 수** | 22개 | 8개 | 30개 |
| **총 비용** | **$51,688.29** | **$3,302.47** | **$54,990.76** |
| **총 단계 수** | 351 steps | 122 steps | 473 steps |
| **총 실행 시간** | 651.34 hours | 602.80 hours | 1,254.14 hours |
| **평균 파이프라인 비용** | $2,349.47 | $412.81 | $1,833.03 |

### 주요 차이점

**Team 2 특징:**
- Single Cell RNA 분석 중심 (전체 비용의 93%)
- 고비용 파이프라인 집중 ($9,000 ~ $10,000/pipeline)
- 주요 플랫폼: Parse Bioscience, 10x Genomics, Scale Bio

**Team 3 특징:**
- Assembly와 Microbiome 분석 중심
- 상대적으로 저비용 구조
- 주요 플랫폼: PacBio Revio, Illumina, Nanopore

---

## Team 2 분석

### 📊 전체 요약

| 항목 | 값 |
|------|-----|
| **총 파이프라인 수** | 22개 |
| **총 그룹 수** | 128 groups |
| **총 분석 단계 수** | 351 steps |
| **총 예상 비용** | **$51,688.29** |
| **총 실행 시간** | 651.34 hours |
| **총 CPU 사용량** | 3,841 cores |
| **총 메모리 사용량** | 9,693 GB |
| **총 스토리지** | 5,929.41 GB |
| **평균 시간당 비용** | $79.37/hour |

---

### 💰 직무별 비용 (Team 2)

#### Single Cell RNA - 5개 파이프라인
- **총 비용**: $48,288.78 (전체의 93.4%)
- **그룹 수**: 22 groups
- **단계 수**: 80 steps
- **실행 시간**: 287.6 hours
- **주요 파이프라인**:
  1. scRNA_parse_kinnex: $10,445.01
  2. scRNA_parse_illumina: $9,812.05
  3. scRNA_10x_illumina: $9,376.85
  4. scRNA_10x_kinnex: $9,355.57
  5. scRNA_scale_illumina: $9,299.30

#### Spatial - 2개 파이프라인
- **총 비용**: $3,114.01 (6.0%)
- **그룹 수**: 3 groups
- **단계 수**: 3 steps
- **주요 파이프라인**:
  1. cosmx: $3,096.60
  2. geomx: $17.41

#### Short RNA Sequencing - 7개 파이프라인
- **총 비용**: $126.92 (0.25%)
- **그룹 수**: 56 groups
- **단계 수**: 165 steps
- **주요 파이프라인**:
  1. RNASeq_BAM_DEG: $42.32
  2. RNASeq_noREF_DEG: $41.44
  3. RNASeq_DEG_AS_SNP: $14.12

#### 기타 분석
- Whole Genome Bisulfite Sequencing: $136.17
- Methylation Chip: $11.63
- Targeted Methylation Sequencing: $6.50
- Long RNA Sequencing: $3.65
- Whole Genome Sequencing: $0.58
- Microarray: $0.05

---

### 🔝 가장 비용이 높은 파이프라인 Top 10 (Team 2)

| 순위 | 직무 | Analysis Name | 비용 (USD) | 시간 (hr) | Groups | Steps |
|------|------|---------------|-----------|----------|--------|-------|
| 1 | Single Cell RNA | scRNA_parse_kinnex | $10,445.01 | 68.5 | 6 | 18 |
| 2 | Single Cell RNA | scRNA_parse_illumina | $9,812.05 | 39.0 | 2 | 7 |
| 3 | Single Cell RNA | scRNA_10x_illumina | $9,376.85 | 37.0 | 2 | 6 |
| 4 | Single Cell RNA | scRNA_10x_kinnex | $9,355.57 | 104.6 | 3 | 24 |
| 5 | Single Cell RNA | scRNA_scale_illumina | $9,299.30 | 38.5 | 9 | 25 |
| 6 | Spatial | cosmx | $3,096.60 | 36.0 | 2 | 2 |
| 7 | WGBS | DMR 분석 - human/mouse 외 | $69.45 | 87.1 | 11 | 16 |
| 8 | WGBS | DMR 분석 - human/mouse | $66.72 | 84.9 | 11 | 15 |
| 9 | Short RNA | RNASeq_BAM_DEG | $42.32 | 50.3 | 10 | 22 |
| 10 | Short RNA | RNASeq_noREF_DEG | $41.44 | 29.1 | 12 | 25 |

---

### 🎯 주요 인사이트 (Team 2)

#### 1. 비용 집중도
- **Single Cell RNA** 파이프라인이 전체 비용의 **93.4%** 차지
- 상위 5개 파이프라인이 전체 비용의 **93.2%** 차지
- 극단적인 비용 편중 현상

#### 2. Single Cell RNA 분석 특징
- 평균 파이프라인 비용: **$9,657.71**
- 주요 비용 발생: **Post-processing** 단계
- 고사양 인스턴스 장시간 사용 (36~104 hours)

#### 3. 비용 최적화 포인트
- **Single Cell RNA Post-processing**: 각 파이프라인당 $9,000 이상 소요
- **Spatial (CosMx)**: 단일 분석에 $3,096 소요
- 이 두 영역에 집중된 최적화로 큰 절감 효과 기대

---

## Team 3 분석

### 📊 전체 요약

| 항목 | 값 |
|------|-----|
| **총 파이프라인 수** | 8개 (Assembly 3개, Microbiome 5개) |
| **총 그룹 수** | 48 groups |
| **총 분석 단계 수** | 122 steps |
| **총 예상 비용** | **$3,302.47** |
| **총 실행 시간** | 602.8 hours |
| **총 CPU 사용량** | 4,924 cores |
| **총 메모리 사용량** | 2,634 GB |
| **총 스토리지** | 4,200.4 GB |
| **평균 시간당 비용** | $5.48/hour |

---

### 💰 직무별 비용 (Team 3)

#### Assembly (유전체 조립) - 3개 파이프라인
- **총 비용**: $1,934.48
- **그룹 수**: 19 groups
- **단계 수**: 54 steps
- **실행 시간**: 211.6 hours
- **CPU 사용량**: 1,689 cores
- **메모리 사용량**: 1,823 GB
- **스토리지**: 3,792 GB
- **평균 단계당 비용**: $35.82

**파이프라인 상세:**
1. **Large Genome Assembly - All** (Human, Animal, Plant)
   - 9 groups, 30 steps
   - CPU: 719 cores, Memory: 1,378 GB
   - $1,772.34

2. **Small Genome Assembly - Bacteria/Fungi**
   - 7 groups, 19 steps
   - CPU: 761 cores, Memory: 52 GB
   - $84.52

3. **Organelle Assembly - CP/MT**
   - 3 groups, 5 steps
   - CPU: 209 cores, Memory: 393 GB
   - $77.62

#### Microbiome (마이크로바이옴) - 5개 파이프라인
- **총 비용**: $1,367.99
- **그룹 수**: 29 groups
- **단계 수**: 68 steps
- **실행 시간**: 391.2 hours
- **CPU 사용량**: 3,235 cores
- **메모리 사용량**: 811 GB
- **스토리지**: 408.4 GB
- **평균 단계당 비용**: $20.12

**파이프라인 상세:**
1. **shotgun metagenome 분석 - Pacbio** (PacBio Revio, HiFi-MAG-Pipeline)
   - 7 groups, 14 steps
   - CPU: 528 cores, Memory: 274 GB
   - $997.53

2. **16S rRNA metagenome - Pacbio** (PacBio Revio, full-length)
   - 6 groups, 19 steps
   - CPU: 1,088 cores, Memory: 264 GB
   - $318.48

3. **shotgun metagenome - Illumina** (Illumina Novaseq)
   - 6 groups, 12 steps
   - CPU: 433 cores, Memory: 170 GB
   - $21.34

4. **16S rRNA metagenome - Microbiome Consortium**
   - 4 groups, 4 steps
   - CPU: 98 cores, Memory: 71 GB
   - $23.16

5. **16S rRNA metagenome - Illumina** (Illumina Miseq, V3-V4)
   - 6 groups, 19 steps
   - CPU: 1,088 cores, Memory: 32 GB
   - $7.48

---

### 🔝 가장 비용이 높은 파이프라인 Top 8 (Team 3)

| 순위 | 직무 | Analysis Name | 비용 (USD) | 시간 (hr) | Groups | Steps |
|------|------|---------------|-----------|----------|--------|-------|
| 1 | Assembly | Large Genome Assembly - All | $1,772.34 | 148.9 | 9 | 30 |
| 2 | Microbiome | shotgun metagenome 분석 - Pacbio | $997.53 | 250.5 | 7 | 14 |
| 3 | Microbiome | 16S rRNA metagenome - Pacbio | $318.48 | 117.9 | 6 | 19 |
| 4 | Assembly | Small Genome Assembly - Bacteria/Fungi | $84.52 | 32.6 | 7 | 19 |
| 5 | Assembly | Organelle Assembly - CP/MT | $77.62 | 30.1 | 3 | 5 |
| 6 | Microbiome | 16S rRNA metagenome - Microbiome Consortium | $23.16 | 9.2 | 4 | 4 |
| 7 | Microbiome | shotgun metagenome - Illumina | $21.34 | 10.6 | 6 | 12 |
| 8 | Microbiome | 16S rRNA metagenome - Illumina | $7.48 | 3.0 | 6 | 19 |

---

### 💸 가장 비용이 높은 분석 단계 Top 10 (Team 3)

| 순위 | 파이프라인 | 단계 | 도구 | 비용 | 인스턴스 | 시간 |
|------|-----------|------|------|------|----------|------|
| 1 | Shotgun metagenome | Assembly | flye | $979.77 | c6i.24xlarge | 240h |
| 2 | Large Genome | Gene Prediction | maker | $871.62 | r6i.16xlarge | 36h × 6 |
| 3 | Large Genome | Assembly (verkko) | verkko | $392.48 | c6i.16xlarge | 18h × 8 |
| 4 | Large Genome | Assembly (nextdenovo) | nextdenovo | $217.70 | c6i.16xlarge | 10h × 8 |
| 5 | 16S rRNA | ASV Clustering | qiime2 | $136.00 | c6i.16xlarge | 50h |
| 6 | Large Genome | Error Correction | nextpolish | $131.04 | c6i.16xlarge | 6h × 8 |
| 7 | 16S rRNA | Phylogeny | qiime2 | $130.66 | c6i.16xlarge | 48h |
| 8 | Small Genome | Assembly | unicycler | $65.28 | c6i.16xlarge | 24h |
| 9 | Large Genome | Assembly (hifiasm+HiC) | hifiasm | $38.11 | c6i.16xlarge | 14h |
| 10 | Large Genome | Assembly (hifiasm) | hifiasm | $32.66 | c6i.16xlarge | 12h |

---

### 🎯 주요 인사이트 (Team 3)

#### 1. 비용 집중 영역
- **상위 3개 파이프라인**이 전체 비용의 **94%** 차지
  - Large Genome Assembly: $1,772 (54%)
  - Shotgun metagenome (PacBio): $998 (30%)
  - 16S rRNA (PacBio): $318 (10%)
- **Gene prediction (maker)**와 **Assembly (flye)** 두 단계가 전체의 **56%**

#### 2. Assembly vs Microbiome 비교

| 구분 | Assembly | Microbiome |
|------|----------|------------|
| 파이프라인 수 | 3개 | 5개 |
| 총 비용 | $1,934 | $1,368 |
| 평균 비용/파이프라인 | $645 | $274 |
| 평균 비용/단계 | $35.82 | $20.12 |
| CPU 사용량 | 1,689 cores | 3,235 cores |
| 메모리 사용량 | 1,823 GB | 811 GB |

**결론**:
- Assembly가 파이프라인당 비용이 2.4배 높음
- Microbiome이 CPU를 2배 더 많이 사용하지만 비용은 더 낮음
- Assembly는 메모리 집약적, Microbiome은 CPU 집약적

#### 3. Compute vs Storage 비용
- **Compute 비용**: $3,298.39 (99.9%)
- **Storage 비용**: $4.07 (0.1%)
- **결론**: 스토리지 최적화보다 **인스턴스 최적화**가 훨씬 중요

---

## 💡 종합 비용 절감 전략

### 🎯 Team 2 최적화 전략 (우선순위 높음)

#### 1. Single Cell RNA Post-processing 최적화
```
현재 비용: $45,000+ (전체의 87%)
목표: 30-40% 절감

조치 사항:
1. Spot Instances 적용 (70% 절감 가능)
   - 예상 절감: $31,500

2. 인스턴스 크기 최적화
   - Post-processing 단계 분석
   - 실제 CPU/메모리 사용률 모니터링
   - 예상 절감: $4,500 (10%)

3. 파이프라인 병렬화 개선
   - 현재: 순차 처리
   - 개선: 샘플별 병렬 처리
   - 시간 단축 → 비용 절감
```

#### 2. Spatial 분석 최적화
```
현재 비용: $3,114
목표: 20-30% 절감

조치 사항:
- CosMx 분석 단계별 검토
- 불필요한 고사양 인스턴스 사용 확인
- 예상 절감: $622-934
```

### 🎯 Team 3 최적화 전략

#### 1. Spot Instances 사용
```
예상 절감액: $2,311 (70% 절감)
적용 대상: 모든 배치 작업

우선 적용:
- Assembly 파이프라인
- Microbiome 파이프라인
```

#### 2. 고비용 작업 타깃 최적화
```
Top 2 비용 작업:
1. Flye assembly ($980):
   - 파라미터 튜닝
   - 대체 도구 검토

2. Maker gene prediction ($872):
   - 병렬 처리 조정
   - 중간 결과 재사용

예상 절감: $200-400
```

### 📊 종합 최적화 효과 예상

| 팀 | 현재 비용 | 최적화 목표 | 예상 절감 | 절감률 |
|-----|----------|------------|----------|--------|
| Team 2 | $51,688 | Spot + 인스턴스 최적화 | $36,000 | 70% |
| Team 3 | $3,302 | Spot + 작업 최적화 | $2,500 | 75% |
| **합계** | **$54,991** | **병행 적용** | **$38,500** | **70%** |

**최적화 후 예상 총 비용**: $16,491 (현재: $54,991)

---

## 📁 주요 파일 위치

### Team 2 파일

**데이터 파일:**
- `data/team2/analysis_raw.csv` - Google Sheets 원본 데이터
- `data/team2/analysis_processed.csv` - 정리된 데이터
- `data/team2/analysis_with_costs.csv` - 비용 계산 포함 데이터

**리포트:**
- `reports/team2/00_SUMMARY_ALL_PIPELINES.txt` - 전체 요약
- `reports/team2/pipeline_summary.csv` - 파이프라인별 요약 (CSV)
- `reports/team2/*_report.txt` - 22개 파이프라인 상세 리포트

### Team 3 파일

**데이터 파일:**
- `data/team3/analysis_raw.csv` - Google Sheets 원본 데이터
- `data/team3/analysis_processed.csv` - 정리된 데이터
- `data/team3/analysis_with_costs.csv` - 비용 계산 포함 데이터

**리포트:**
- `reports/team3/00_SUMMARY_ALL_PIPELINES.txt` - 전체 요약
- `reports/team3/pipeline_summary.csv` - 파이프라인별 요약 (CSV)
- `reports/team3/*_report.txt` - 8개 파이프라인 상세 리포트

### 공통 스크립트

```bash
# Team 2 분석
python3 scripts/01_process_data.py 2
python3 scripts/02_calculate_aws_costs.py 2
python3 scripts/03_analyze_pipelines.py 2

# Team 3 분석
python3 scripts/01_process_data.py 3
python3 scripts/02_calculate_aws_costs.py 3
python3 scripts/03_analyze_pipelines.py 3
```

---

**분석 완료일**: 2026-01-06
**분석 대상**: Team 2 (22 pipelines), Team 3 (8 pipelines)
**총 파이프라인**: 30개
**다음 업데이트**: 분기별 또는 파이프라인 변경 시
