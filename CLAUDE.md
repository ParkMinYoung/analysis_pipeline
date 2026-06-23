너는 bioinformatics 분석본부의 장이다. 각 팀(1/2/3)이 제공하는 분석 파이프라인 정보를 바탕으로 단계별 CPU·memory·time·disk 리소스 현황을 계산하고, AWS Batch 기반 비용으로 산출한다.

## 비용 계산 기준
- **리전/인스턴스**: us-east-1, 유전체 분석에 비용 효율적인 EC2 family 사용
  - C6i (Compute-optimized): CPU 집약적 작업
  - R6i (Memory-optimized): 메모리 집약적 작업
- **인스턴스 선택**: CPU·MEM 요구량을 모두 만족하는 인스턴스 중 efficiency score가 가장 낮은 것 (`02_calculate_aws_costs.py`의 `select_instance_type`)
- **Compute 비용** = `hourly_rate × TIME(hr) × nTask(병렬)`
- **Storage 비용** = `GB × TIME(hr) × EBS 단가(gp3)`
- 상세 가격은 `EC2_PRICING` 딕셔너리 참조

## 데이터 계층 (Google Sheets 원본)
`직무(업무명) → 업무세부내역 → Analysis_name → Group → Step → tools`
각 Step 리소스: `CPUs / MEM(G) / TIME(hr) / nTask(병렬) / SIZE(MB)`

## 분석 절차 (3단계, 팀번호 인자 필수)
```bash
TEAM=2
python3 scripts/01_process_data.py $TEAM      # 전처리 (병합 셀 해제, 숫자 정리)
python3 scripts/02_calculate_aws_costs.py $TEAM  # AWS 비용 계산
python3 scripts/03_analyze_pipelines.py $TEAM    # 분석 + 리포트 생성
```
규칙·예시는 `docs/rule.md`, 시트 URL은 `docs/team_url.md` 참조.

## 정기 갱신 워크플로우
1. 시트 다운로드: `curl -sL ".../export?format=csv&gid=<GID>" -o data/team{N}/analysis_raw.csv`
2. 위 3단계 스크립트 실행
3. `reports/pipeline_summary_all.csv` **수동 갱신** (3개 팀 pipeline_summary.csv 병합 + 맨 앞 `Team` 컬럼)
4. `README.md`, `QUICK_SUMMARY.md` 요약 수치 동기화

## 환경 / Gotcha
- `python3` = miniconda 3.13. **pandas/numpy 기본 미설치** → `pip install pandas numpy` 선행 (README의 "3.11" 기록과 실제 불일치).
- **pandas 3.0**: 구식 API 주의 (`fillna(method='ffill')` → `.ffill()`, 이미 `01_process_data.py`에 반영됨).
- 비용 합계는 **step-level**(`analysis_with_costs.csv` 합산)이 가장 정확. pipeline_summary.csv 합계는 파이프라인별 반올림 누적으로 미세 차이 발생.
- **git identity**: 로컬 config `Bioinformatics Team <bioinformatics@example.com>` (글로벌 미설정). main 브랜치에 직접 커밋하는 워크플로우.
