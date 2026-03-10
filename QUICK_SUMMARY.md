# 생물정보 분석 파이프라인 비용 분석 - 빠른 요약

## 목차 (Table of Contents)

1. [전체 요약 (Team 1 + Team 2 + Team 3)](#전체-요약)
2. [Team 1 분석 (19 pipelines)](#team-1-분석)
3. [Team 2 분석 (22 pipelines)](#team-2-분석)
4. [Team 3 분석 (8 pipelines)](#team-3-분석)
5. [주요 파일 위치](#주요-파일-위치)

---

## 전체 요약

### 3개 팀 통합 현황

| 항목 | Team 1 | Team 2 | Team 3 | 합계 |
|------|--------|--------|--------|------|
| **파이프라인 수** | 19개 | 22개 | 8개 | 49개 |
| **총 비용** | **$14,045.62** | **$505.14** | **$3,302.47** | **$17,853.23** |
| **총 단계 수** | 338 steps | 354 steps | 122 steps | 814 steps |
| **총 실행 시간** | 382.64 hours | 534.04 hours | 602.80 hours | 1,519.48 hours |
| **평균 파이프라인 비용** | $739.24 | $22.96 | $412.81 | $364.35 |

### 주요 특징

**Team 1 특징:**
- 다양한 분석 영역 커버 (WGS, WES, DNA Chip, Pangenome, 커스텀 분석)
- PWAS(커스텀 분석)가 전체 비용의 92.0% 차지
- 주요 플랫폼: PacBio Revio, Illumina NovaSeq, Axiom/Illumina Microarray

**Team 2 특징:**
- 9개 직무 영역의 다양한 파이프라인 보유 (Short RNA, Single Cell RNA, WGBS, Spatial 등)
- 비용이 고르게 분산된 구조
- 주요 플랫폼: Illumina NovaSeq, PacBio Revio, 10x Genomics, Parse Bioscience

**Team 3 특징:**
- Assembly와 Microbiome 분석 중심
- 장시간 실행 작업 집중 (602.80 hours)
- 주요 플랫폼: PacBio Revio, Illumina, Nanopore

---

## Team 1 분석

### 전체 요약

| 항목 | 값 |
|------|-----|
| **총 파이프라인 수** | 19개 |
| **총 그룹 수** | 185 groups |
| **총 분석 단계 수** | 338 steps |
| **총 예상 비용** | **$14,045.62** |
| **총 실행 시간** | 382.64 hours |
| **총 CPU 사용량** | 2,171 cores |
| **총 메모리 사용량** | 6,277 GB |
| **총 스토리지** | 1,814.40 GB |

---

### 직무별 비용 (Team 1)

#### 커스텀 분석 - 2개 파이프라인
- **총 비용**: $13,103.86 (전체의 93.3%)
- **그룹 수**: 25 groups
- **단계 수**: 37 steps
- **주요 파이프라인**:
  1. PWAS (Proteome-Wide Association Study): $12,926.15
  2. Kinics-ICS: $177.71

#### Whole Genome Sequencing - 3개 파이프라인
- **총 비용**: $732.98 (5.2%)
- **그룹 수**: 37 groups
- **단계 수**: 126 steps
- **주요 파이프라인**:
  1. PacBio Revio Human WGS: $257.48
  2. Illumina NovaSeq non-Human WGS: $227.64
  3. Illumina NovaSeq Human WGS: $216.80

#### 기타 분석
- Pangenome (Fungi): $154.80
- Whole Exome Sequencing: $27.36
- DNA Chip: $25.57
- 단백질 데이터 통계 분석: $1.05

---

### 가장 비용이 높은 파이프라인 Top 10 (Team 1)

| 순위 | 직무 | Analysis Name | 비용 (USD) | 시간 (hr) | Groups | Steps |
|------|------|---------------|-----------|----------|--------|-------|
| 1 | 커스텀 분석 | PWAS | $12,926.15 | 92.8 | 24 | 31 |
| 2 | WGS | PacBio Revio Human WGS | $257.48 | 66.6 | 6 | 34 |
| 3 | WGS | Illumina NovaSeq non-Human WGS | $227.64 | 48.1 | 17 | 32 |
| 4 | WGS | Illumina NovaSeq Human WGS | $216.80 | 82.4 | 24 | 46 |
| 5 | 커스텀 분석 | Kinics-ICS | $177.71 | 33.7 | 1 | 6 |
| 6 | Pangenome | Fungi Pangenome construction | $154.80 | 14.0 | 4 | 4 |
| 7 | WGS | Illumina NovaSeq Human SV | $31.06 | 5.9 | 7 | 14 |
| 8 | DNA Chip | Post-GWAS downstream | $21.09 | 8.8 | 6 | 19 |
| 9 | WES | Illumina NovaSeq Germline CNV | $16.43 | 4.1 | 16 | 18 |
| 10 | WES | Illumina NovaSeq Human WES | $7.05 | 9.2 | 24 | 44 |

---

### 가장 비용이 높은 분석 단계 Top 5 (Team 1)

| 순위 | 파이프라인 | 단계 | 도구 | 비용 | 인스턴스 | 시간 |
|------|-----------|------|------|------|----------|------|
| 1 | PWAS | FUSION_wgt | R | $12,794.94 | c6i.16xlarge | 84h x 56 |
| 2 | PacBio WGS | pbmm2_align_wgs | pbmm2 | $190.43 | c6i.16xlarge | 5h x 14 |
| 3 | Pangenome | Correction & Scaffolding | RagTag/TGS | $140.35 | r6i.16xlarge | 8.7h x 4 |
| 4 | Non-Human WGS | Variant Annotation | perl | $123.77 | c6i.4xlarge | 0.5h x 364 |
| 5 | PWAS | PWASO_Model | TIGAR | $119.68 | c6i.16xlarge | 2h x 22 |

---

### 주요 인사이트 (Team 1)

#### 1. 비용 집중도
- **PWAS (커스텀 분석)** 파이프라인이 전체 비용의 **92.0%** 차지
- FUSION_wgt 단일 단계가 전체 비용의 **91.1%** 차지

#### 2. PWAS 분석 특징
- FUSION_wgt 단계: c6i.16xlarge (64 vCPU, 32GB) x 56 병렬 작업
- 84시간 장시간 실행

#### 3. 비용 최적화 포인트
- **PWAS FUSION_wgt**: $12,795 -> Spot Instance 적용 시 약 $3,838 (70% 절감)
- **WGS 파이프라인**: 비교적 합리적인 비용 구조
- **DNA Chip & WES**: 매우 저비용 구조

---

## Team 2 분석

### 전체 요약

| 항목 | 값 |
|------|-----|
| **총 파이프라인 수** | 22개 |
| **총 그룹 수** | 129 groups |
| **총 분석 단계 수** | 354 steps |
| **총 예상 비용** | **$505.14** |
| **총 실행 시간** | 534.04 hours |
| **총 CPU 사용량** | 2,269 cores |
| **총 메모리 사용량** | 7,462 GB |
| **총 스토리지** | 5,935.40 GB |

---

### 직무별 비용 (Team 2)

#### Single Cell RNA - 5개 파이프라인
- **총 비용**: $169.25 (전체의 33.5%)
- **그룹 수**: 17 groups
- **단계 수**: 80 steps
- **주요 파이프라인**:
  1. scRNA_parse_kinnex: $50.36
  2. scRNA_10x_kinnex: $40.96
  3. scRNA_parse_illumina: $30.08
  4. scRNA_10x_illumina: $24.63
  5. scRNA_scale_illumina: $23.22

#### Whole Genome Bisulfite Sequencing - 2개 파이프라인
- **총 비용**: $136.17 (27.0%)
- **그룹 수**: 11 groups
- **단계 수**: 31 steps
- **주요 파이프라인**:
  1. WGBS DMR 분석 - human/mouse 외: $69.45
  2. WGBS DMR 분석 - human/mouse: $66.72

#### Short RNA Sequencing - 7개 파이프라인
- **총 비용**: $128.64 (25.5%)
- **그룹 수**: 33 groups
- **단계 수**: 168 steps
- **주요 파이프라인**:
  1. RNASeq_BAM_DEG: $44.04
  2. RNASeq_noREF_DEG: $41.44
  3. RNASeq_DEG_AS_SNP: $14.12

#### Spatial - 2개 파이프라인
- **총 비용**: $48.68 (9.6%)
- **주요 파이프라인**:
  1. cosmx: $48.41
  2. geomx: $0.27

#### 기타 분석
- Methylation Chip: $11.63
- Targeted Methylation Sequencing: $6.50
- Long RNA Sequencing: $3.65
- Whole Genome Sequencing: $0.58
- Microarray: $0.05

---

### 가장 비용이 높은 파이프라인 Top 10 (Team 2)

| 순위 | 직무 | Analysis Name | 비용 (USD) | 시간 (hr) | Groups | Steps |
|------|------|---------------|-----------|----------|--------|-------|
| 1 | WGBS | WGBS DMR 분석 - human/mouse 외 | $69.45 | 87.1 | 11 | 16 |
| 2 | WGBS | WGBS DMR 분석 - human/mouse | $66.72 | 84.9 | 11 | 15 |
| 3 | Single Cell RNA | scRNA_parse_kinnex | $50.36 | 44.5 | 6 | 18 |
| 4 | Spatial | cosmx | $48.41 | 36.0 | 2 | 2 |
| 5 | Short RNA | RNASeq_BAM_DEG | $44.04 | 53.0 | 11 | 25 |
| 6 | Short RNA | RNASeq_noREF_DEG | $41.44 | 29.1 | 12 | 25 |
| 7 | Single Cell RNA | scRNA_10x_kinnex | $40.96 | 80.6 | 3 | 24 |
| 8 | Single Cell RNA | scRNA_parse_illumina | $30.08 | 15.0 | 2 | 7 |
| 9 | Single Cell RNA | scRNA_10x_illumina | $24.63 | 13.0 | 2 | 6 |
| 10 | Single Cell RNA | scRNA_scale_illumina | $23.22 | 14.5 | 9 | 25 |

---

### 가장 비용이 높은 분석 단계 Top 5 (Team 2)

| 순위 | 파이프라인 | 단계 | 도구 | 비용 | 인스턴스 | 시간 |
|------|-----------|------|------|------|----------|------|
| 1 | cosmx | Post-processing | Giotto | $48.40 | r6i.16xlarge | 12h |
| 2 | WGBS human/mouse | BISMARK | bismark | $47.29 | c6i.8xlarge | 34.5h |
| 3 | WGBS human/mouse 외 | BISMARK_ALIGN | bismark | $47.29 | c6i.8xlarge | 34.5h |
| 4 | RNASeq_noREF_DEG | Assembly | Trinity | $24.48 | c6i.24xlarge | 6h |
| 5 | scRNA_10x_illumina | integration_annot | Seurat | $16.15 | r6i.8xlarge | 8h |

---

### 주요 인사이트 (Team 2)

#### 1. 비용 분산 구조
- 비용이 3개 직무에 고르게 분산: Single Cell RNA (33.5%), WGBS (27.0%), Short RNA (25.5%)
- 가장 고비용 파이프라인이 $69.45로 비교적 저비용

#### 2. 주요 비용 발생 단계
- **BISMARK alignment** (WGBS): 34.5시간 장시간 실행
- **Post-processing** (cosmx Spatial): r6i.16xlarge 메모리 집약적 분석
- **integration_annot** (Single Cell RNA): Seurat 기반 200GB 메모리 사용

#### 3. 비용 최적화 포인트
- 전체 비용이 $505로 이미 효율적인 구조
- Spot Instance 적용 시 추가 70% 절감 가능

---

## Team 3 분석

### 전체 요약

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

---

### 직무별 비용 (Team 3)

#### Assembly (유전체 조립) - 3개 파이프라인
- **총 비용**: $1,934.48
- **그룹 수**: 16 groups
- **단계 수**: 54 steps
- **실행 시간**: 211.6 hours
- **CPU 사용량**: 1,689 cores
- **메모리 사용량**: 1,823 GB
- **스토리지**: 3,792 GB

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
- **그룹 수**: 15 groups
- **단계 수**: 68 steps
- **실행 시간**: 391.2 hours
- **CPU 사용량**: 3,235 cores
- **메모리 사용량**: 811 GB
- **스토리지**: 408.4 GB

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

### 가장 비용이 높은 파이프라인 Top 8 (Team 3)

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

### 가장 비용이 높은 분석 단계 Top 10 (Team 3)

| 순위 | 파이프라인 | 단계 | 도구 | 비용 | 인스턴스 | 시간 |
|------|-----------|------|------|------|----------|------|
| 1 | Shotgun metagenome | Assembly | flye | $979.77 | c6i.24xlarge | 240h |
| 2 | Large Genome | Gene Prediction | maker | $871.62 | r6i.16xlarge | 36h x 6 |
| 3 | Large Genome | Assembly (verkko) | verkko | $392.48 | c6i.16xlarge | 18h x 8 |
| 4 | Large Genome | Assembly (nextdenovo) | nextdenovo | $217.70 | c6i.16xlarge | 10h x 8 |
| 5 | 16S rRNA Pacbio | ASV Clustering | qiime2 | $136.00 | c6i.16xlarge | 50h |
| 6 | Large Genome | Error Correction | nextpolish | $131.04 | c6i.16xlarge | 6h x 8 |
| 7 | 16S rRNA Pacbio | Phylogeny | qiime2 | $130.66 | c6i.16xlarge | 48h |
| 8 | Small Genome | Assembly | unicycler | $65.28 | c6i.16xlarge | 24h |
| 9 | Large Genome | Assembly (hifiasm+HiC) | hifiasm | $38.11 | c6i.16xlarge | 14h |
| 10 | Large Genome | Assembly (hifiasm) | hifiasm | $32.66 | c6i.16xlarge | 12h |

---

### 주요 인사이트 (Team 3)

#### 1. 비용 집중 영역
- **상위 3개 파이프라인**이 전체 비용의 **93%** 차지
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

## 종합 비용 절감 전략

### Team 1 최적화 전략 (최우선순위)

#### 1. PWAS FUSION_wgt 최적화
```
현재 비용: $12,795 (전체의 91.1%)
목표: 70% 절감

조치 사항:
1. Spot Instances 적용 (최우선)
   - 예상 절감: $8,957 (70%)
   - 최종 비용: $3,838

2. 병렬 작업 수 조정
   - 현재: 56 parallel tasks
   - 검토: 최적 병렬 수 분석

3. 알고리즘 최적화
   - FUSION 파라미터 튜닝
   - 중간 결과 캐싱
```

### Team 2 최적화 전략

```
현재 비용: $505 (이미 효율적)
Spot Instances 적용 시: ~$152 (70% 절감)
추가 최적화 여지: 제한적
```

### Team 3 최적화 전략

#### 1. Spot Instances 사용
```
예상 절감액: $2,312 (70% 절감)
적용 대상: 모든 배치 작업
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
```

### 종합 최적화 효과 예상

| 팀 | 현재 비용 | 예상 절감 | 절감률 | 최적화 후 |
|-----|----------|----------|--------|----------|
| Team 1 | $14,046 | $8,957 | 64% | $5,089 |
| Team 2 | $505 | $354 | 70% | $152 |
| Team 3 | $3,302 | $2,312 | 70% | $991 |
| **합계** | **$17,853** | **$11,623** | **65%** | **$6,231** |

---

## 주요 파일 위치

### Team 1 파일

**데이터 파일:**
- `data/team1/analysis_raw.csv` - Google Sheets 원본 데이터
- `data/team1/analysis_processed.csv` - 정리된 데이터
- `data/team1/analysis_with_costs.csv` - 비용 계산 포함 데이터

**리포트:**
- `reports/team1/00_SUMMARY_ALL_PIPELINES.txt` - 전체 요약
- `reports/team1/pipeline_summary.csv` - 파이프라인별 요약 (CSV)
- `reports/team1/*_report.txt` - 19개 파이프라인 상세 리포트

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
# 전체 팀 한번에 실행
for team in 1 2 3; do
  python3 scripts/01_process_data.py $team && \
  python3 scripts/02_calculate_aws_costs.py $team && \
  python3 scripts/03_analyze_pipelines.py $team
done
```

---

**분석 완료일**: 2026-03-10
**분석 대상**: Team 1 (19 pipelines), Team 2 (22 pipelines), Team 3 (8 pipelines)
**총 파이프라인**: 49개
**총 예상 비용**: $17,853.23
