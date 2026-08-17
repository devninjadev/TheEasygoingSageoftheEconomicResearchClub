# World Memory 개인 읽기 브리지

이 파일은 사용자가 승인한 개인 Notion 저장소의 불변 읽기 위치를 기록한다. 인증정보나 실행 상태를 포함하지 않는다.

## Hub

- URL: `https://app.notion.com/p/devninja/World-Memory-Notion-Native-3bc2f5b14f3b81769245c8356b8b3072?source=copy_link`
- 제목: `World Memory · Notion Native`
- 계약 표식: `World Memory storage contract: notion-native-v2`

제목만 같은 페이지를 채택하지 않는다. Hub URL과 계약 표식을 모두 확인한다.

## 데이터 소스

| 역할 | 데이터 소스 ID | 데이터베이스 ID |
|---|---|---|
| Collections | `7ade603e-4679-4ec4-a649-9eee37aaf5f3` | `5a73e9a73aae49c59c303a5e49475b48` |
| Stories | `70d9d79e-0731-4c0a-85c3-8fdddf8b747b` | `a96636ccb58b43c1aec1b687149cd769` |
| Reports | `77f9c6e9-3636-4696-b2b1-e71efe2cfdd0` | `02f42d94e35f4472b370f659ee364083` |
| Story Changes | `a77292d7-72a6-486f-9c17-049d0e5e66f8` | `1c6081c4a48a468c885a8f94ea36ea0e` |

## 저장 뷰

### Reports Recent

- View ID: `3bc2f5b1-4f3b-81c4-83ec-000c8732c5e5`
- Query URL: `https://app.notion.com/p/02f42d94e35f4472b370f659ee364083?v=3bc2f5b14f3b81c483ec000c8732c5e5`

### Stories Current

- View ID: `3bc2f5b1-4f3b-8102-af15-000c67d7b019`
- Query URL: `https://app.notion.com/p/a96636ccb58b43c1aec1b687149cd769?v=3bc2f5b14f3b8102af15000c67d7b019`

두 뷰 모두 공식 Notion 데이터베이스 조회에서 `data.mode=view`, `is_archived:false`, `page_size:100`을 사용한다. 저장 뷰의 필터·정렬·표시 속성을 유지하고 관련 현재 Story와 최근 Report만 읽는다.

## 읽기 절차

1. 정확한 Hub와 계약 표식을 확인한다.
2. `Stories Current`에서 관련 미해결 현재 가설을 읽는다.
3. 필요할 때 `Reports Recent`의 관련 보고서를 읽는다.
4. 관찰·생성 시각, 신뢰도, 가설, 반대 근거, 무효화 조건을 보존한다.
5. 현재 증거와 비교해 `strengthened`, `weakened`, `maintained`, `unresolved` 중 하나로 분류한다.
6. 충돌하면 현재 사실을 덮어쓰지 않고 충돌을 설명한다.

정확한 저장 뷰 읽기가 실패하면 같은 뷰에 한 번만 재시도한다. 두 번째 실패 뒤에는 World Memory 없이 계속한다. 제목 검색, 광범위 의미 검색, 다른 Hub 추측, SQL, 스키마 수리나 마이그레이션으로 우회하지 않는다.

## 쓰기 경계

자동 읽기는 허용되지만 자동 쓰기는 허용되지 않는다. `참고해`, `기억해 둬`, `앞으로 고려해`는 쓰기 승인이 아니다.

`월드메모리에 저장해`, `새 Story로 기록해`, `기존 가설을 갱신해`, `월드메모리 리포트를 실행해`처럼 명시적인 요청만 쓰기 워크플로 입구가 된다. 그 경우에도 명희가 직접 변형하지 않고 `$world-memory-autopilot`의 확인·안전중단·쓰기 영수증 계약에 위임한다. 명시적 쓰기 의도가 없으면 Collection, Report, Story, Story Change의 생성·수정, 일정 실행, 설정, 수리, 이동, 삭제, 스키마 변경을 금지한다.

