---
name: update-pipeline-costs
description: 3개 분석 팀(Team 1/2/3)의 Google Sheets 파이프라인 데이터를 다운로드해 기존과 비교하고, 변경이 있을 때만 AWS Batch 비용 재계산·리포트 재생성·문서 동기화·git push를 수행. 변경이 없으면 중단. 파이프라인 비용 갱신/데이터 업데이트/refresh 시 사용.
---

# 파이프라인 비용 갱신 (update-pipeline-costs)

생물정보 분석본부 3개 팀의 파이프라인 데이터를 Google Sheets에서 동기화해 AWS Batch 비용을 재산출하고, 결과·문서·git까지 한 번에 정합.

## 🔒 보안 규칙 (최우선)

- **시트 주소(gid, doc id, URL)는 절대 본 파일·커밋 메시지·리포트에 평문으로 적지 않는다.** 항상 `docs/team_url.md`에서 런타임에 읽어 조립한다.
- 다운로드한 CSV 내용을 화면/로그에 통째로 덤프할 때도 민감 식별자(doc id)가 노출되지 않도록 주의한다.
- 산출물 보고에는 팀명·통계 수치만 사용한다.
- `docs/team_url.md` 자체가 외부 노출되어 있으면 별도 보고(하단 '알려진 보안 이슈' 참고).

## 사전 조건

- 역할: bioinformatics 분석본부장. AWS EC2(us-east-1, C6i/R6i) 기반 Batch 비용 산출. 상세 규칙은 `docs/rule.md`, 구조는 `CLAUDE.md` 참조.
- 대상: Team 1/2/3 각각 `data/team{N}/analysis_raw.csv`.

## 단계 0 — 환경 및 AWS 가격 최신성 확인

1. **환경**: `python3 -c "import pandas, numpy"` 로 확인. 없으면 `pip install pandas numpy` (사용자에게 1회 확인 후 설치).
2. **pandas 3.0 호환성**: `scripts/01_process_data.py` 가 `.ffill()` 을 쓰는지 확인 (`fillna(method='ffill')` 금지).
3. **AWS 가격 최신성** (사용자 요구: 항상 최신):
   - `scripts/02_calculate_aws_costs.py` 의 `EC2_PRICING` 주석의 기준 연월 확인.
   - 대표 2종(c6i.16xlarge, r6i.16xlarge)을 웹(AWS 공식 / instances.vantage.sh)과 교차 확인.
   - **가격이 바뀌었으면** `EC2_PRICING` 전체 갱신 + 주석 날짜 수정 + 비용 영향을 단계 7 요약에 포함. 바뀌지 않았으면 "이미 최신" 기록.

## 단계 1 — 각 팀 시트 다운로드

`docs/team_url.md` 에서 각 팀의 `gid` 를 추출(평문 출력 금지). export URL을 조립해 받되, 기존 파일을 직접 덮어쓰지 말고 **임시 파일로 먼저 받아 비교**:

```bash
# gid 변수만 세팅 (값을 화면에 출력하지 않을 것)
curl -sL "https://docs.google.com/spreadsheets/d/<DOC_ID>/export?format=csv&gid=<GID>" \
  -o /tmp/team${TEAM}_new.csv -w "team${TEAM}: HTTP %{http_code}, %{size_download} bytes\n"
```

3팀(Team=1,2,3) 모두 수행. HTTP 200 + size>0 확인.

## 단계 2 — 변경 여부 확인 (변경 없으면 STOP)

각 팀에 대해 기존 `data/team{N}/analysis_raw.csv` 와 임시 파일을 diff:

```bash
diff data/team${TEAM}/analysis_raw.csv /tmp/team${TEAM}_new.csv
```

- **어느 팀도 변경 없으면**: 임시 파일 삭제 후 **즉시 중단**. "변경 사항 없음 — 종료" 보고하고 끝낸다.
- **1개 이상 변경이 있으면**: 해당 팀만 단계 3 이후 진행(변경 없는 팀은 스킵). 변경된 팀 목록과 변경 규모(증감 행 수)를 기록.

## 단계 3 — 데이터 무결성 검증 (이상 테이블 리포트)

사용자 요구: "table 작성이 사용자 작성과 상이할 경우 관련 부분 리포트". 다음을 점검하고 이상 시 즉시 사용자에게 리포트(자동 수정 금지):

1. **헤더 일치**: 기존과 동일한 컬럼 순서/이름인지.
2. **필수 컬럼 존재**: `직무(업무명), Analysis_name, Group, Step, tools, CPUs, MEM(G), TIME(hr), nTask(병렬), SIZE(MB)`.
3. **숫자 필드 범위**: CPUs/MEM/TIME/nTask/SIZE 에 음수·비정상 대값(예: CPU 수백·TIME 수천) 없는지.
4. **행 수 급변**: ±50% 이상 변동이면 경고(의도적 대량 추가인지 확인 필요).
5. **병합 잔류**: forward-fill 후에도 `직무(업무명)`/`Analysis_name` 빈칸이 남는지.

이상 발견 시 → 리포트 후 사용자 확인 대기. 정상이면 임시 파일을 `data/team{N}/analysis_raw.csv` 로 반영.

## 단계 4 — 스크립트 실행 (변경된 팀만)

```bash
TEAM=<N>
python3 scripts/01_process_data.py $TEAM      # 전처리
python3 scripts/02_calculate_aws_costs.py $TEAM  # AWS 비용 계산
python3 scripts/03_analyze_pipelines.py $TEAM    # 분석 + 리포트 생성
```

각 단계 exit code 확인. 실패 시 stderr tail 출력 후 중단·원인 분석.

## 단계 5 — 통합 요약 갱신 (수동)

`reports/pipeline_summary_all.csv` 는 어떤 스크립트도 자동 생성하지 않는다. 3개 팀 `pipeline_summary.csv` 를 병합:

```python
import pandas as pd
frames = []
for t in [1,2,3]:
    df = pd.read_csv(f'reports/team{t}/pipeline_summary.csv')
    df.insert(0, 'Team', t)
    frames.append(df)
pd.concat(frames, ignore_index=True).to_csv('reports/pipeline_summary_all.csv', index=False)
```

(tools_list 에 쉼표가 있어 텍스트 concat 금지 — 반드시 pandas 병합.)

## 단계 6 — 최신 수치 반영 및 검토

**가장 정확한 비용은 step-level 합산**(`analysis_with_costs.csv` 의 `total_cost_usd` 합). pipeline_summary 합계는 파이프라인별 반올림 누적으로 미세 차이 — 총비용은 step-level 기준 사용.

```bash
python3 -c "import pandas as pd; [print(f'Team {t}:', round(pd.read_csv(f'data/team{t}/analysis_with_costs.csv')['total_cost_usd'].sum(),2)) for t in [1,2,3]]"
```

변경된 팀/직무의 Top 파이프라인·Top 단계 재추출 후 `README.md`, `QUICK_SUMMARY.md` 의 해당 수치(파이프라인 수·비용·steps·시간·Top 표)를 갱신. 완료 후 잔존 outdated 값 grep 확인:

```bash
grep -nE '<이전비용>|<이전파이프라인수>|<이전steps>' README.md QUICK_SUMMARY.md
```

## 단계 7 — 주요 변경 사항 요약 + git push

1. **변경 요약 작성**: 신규/제거 파이프라인, 비용 전후(Δ), 고비용 단계 변동, AWS 가격 변경 영향(있으면).
2. **commit**: 로컬 identity `Bioinformatics Team <bioinformatics@example.com>`(글로벌 미설정 시 로컬 config).
   ```bash
   git add -A && git commit -m "<요약>"
   ```
3. **push**: 사용자 명시 요청 시에만.
   ```bash
   git push origin main
   ```

## 검증 체크리스트 (완료 전)

- [ ] 변경된 팀만 처리했는가 (변경 없는 팀 스킵)
- [ ] step-level 비용으로 총합 산출했는가
- [ ] README/QUICK_SUMMARY 잔존 outdated 수치 0건
- [ ] pipeline_summary_all.csv 갱신됨
- [ ] 보고에 시트 URL/gid 평문 없음
- [ ] commit 메시지에 민감값 없음

## 알려진 보안 이슈

`docs/team_url.md` 가 공개 repo에 URL 평문으로 커밋되어 있을 수 있음. 발견 시 근본 해결(시트 공유 권한 '제한' 변경 / `.gitignore` + `git rm --cached`)은 사용자 승인 후 진행. skill 실행 중에는 추가 노출을 막는 것(본문 평문 금지)만 담당.
