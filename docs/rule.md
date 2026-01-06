
## 1단계
 - 분석 파이프라인을 설명하는 정보를 가져와서 하나의 파일로 저장
 - 사람이 보기 편하게 되어 있다보니, cell 이 병합되어 있는데, 이를 데이터 분석 편의성을 위해서 병합을 해제하고 빈칸에 동일한 문자열로 채움

## 2단계 aws 비용 체계 적용
 - 유전체 분석에 가장 많이 사용되는 cpu family 를 선택하여 해당 비용 쳬계를 적용
 - cpu, memory, 사용 용량을 고려해서 aws batch 과금 기준을 사용
 - region 은 가장 많이 사용되는 region 기준

## 3단계
 - 해당 시트는 직무(엄무명), Analysis_name을 기준으로 분석 파이프라인이 어떻게 구성이 되는지 Group, step 으로 나누어짐
 - 이 때 각 Group, step 에 사용되는 분석은 tools 이라는 컬럼으로 정의
 - 다음의 예시를 가지고 테이블을 이해함.
  - Large Genome Assembly(human) 는 Pacbio Revio 장비료 생산한 데이터를 기반으로 하는 분석 파이프라인이고,
  - inhouse script 로 작성된 1.0.0 version 임
  - 9의 group 분석으로 이루어져 있으며, MAKE_DATASET group 분석은 3개의 step 으로 구성
  - BAM_TO_FASTQ 의 경우는 1.9 버전의 samtools 를 사용하며, CPU 4, MEM 1G, 0.1 hr 시간동안 1 nTask 가 진행되며, 250000MB 를 사용함.

## 4단계
 - 앞서 예시로 설명된 Large Genome Assembly(human) 을 사용시 aws batch 사용 비용 계산
 - 각 직무, 업무세부내역에 따른 aws batch 사용 비용 계산
  - 시간, 메모리, cpu, ntask 를 고려한 계산 적용 
  - 사용되는 group, step 수 및 tools list

