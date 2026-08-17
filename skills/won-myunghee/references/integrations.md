# 선택적 스킬과 플러그인 연동

## 가용성 판정

필요한 기능마다 `available`, `unavailable`, `unknown` 중 하나로 판정한다. 현재 컨텍스트의 스킬 목록이나 실제 호출 가능한 도구만 증거로 삼는다. 스킬 설치와 플러그인·커넥터 연결은 별도 상태다. `unknown`을 설치됨으로 추정하지 않는다.

필요한 스킬이 없으면 실행한 척하지 않고 제한과 정확한 설치 후보를 알린다. 자동 설치는 사용자의 명시적 요청이 있을 때만 가능하다.

| 내부 스킬 | 정본 저장소 |
|---|---|
| `$evidence-first-portfolio-advisor` | `https://github.com/devninjadev/PortfolioAnalysisSkillChatGPT` |
| `$world-memory-autopilot` | `https://github.com/devninjadev/WorldMemoryLite` |
| `$market-news-radar` | `https://github.com/devninjadev/market-news-radar` |

## PortfolioAnalysisSkillChatGPT

기업가치, 현재 가격, 포트폴리오 적합성, 백테스트와 구조화된 차트에는 `$evidence-first-portfolio-advisor`를 적극 사용한다. 핵심 경로와 제공자 우선순위는 설치된 스킬의 최신 계약을 따른다.

- **Alpaca 플러그인:** 적격 미국 주식·암호화폐 가격 폴백, 시장 시계, ETF 시장 폭 확인에 쓰일 수 있다.
- **공식 Wolfram 플러그인:** 후순위 가격·환율, 구조화된 미국 국채 또는 정확한 계산 근거에 쓰일 수 있다.

성공한 선순위 값을 복제하려고 모든 플러그인을 호출하지 않는다. 제공자, 상품 정체성, 통화, 단위, 날짜와 가격 기준을 폴백 사이에서 보존한다.

## WorldMemoryLite

필수 커넥터는 승인된 워크스페이스에 접근 가능한 공식 **Notion** 커넥터다. 스킬 설치만으로 개인 World Memory가 연결됐다고 판단하지 않는다. 명희의 자동 경로는 [world-memory-read-bridge.md](world-memory-read-bridge.md)의 정확한 저장 뷰 읽기까지만 소유한다. 쓰기·예약·수리·마이그레이션은 명시적 요청 뒤 `$world-memory-autopilot`에 위임한다.

## market-news-radar

현재 시장 사건, 속보, 발표와 뉴스 흐름에는 `$market-news-radar`를 사용한다. 오래된 페르소나 프롬프트에 있던 하드코딩 RSS 주소를 사용하지 않고 설치된 스킬의 최신 등록부와 원출처 확인 계약을 따른다.

시장 확인용 **Alpaca**가 없더라도 뉴스 브리핑은 제한적으로 가능할 수 있으나, 시장 시계나 ETF 폭 확인을 수행하지 못했다면 밝힌다.

## 결합 순서

관련 과거 가설이 필요한 경우 World Memory 읽기 → 현재 사건이 중요한 경우 시장 뉴스 → 기업·가격·포트폴리오 계산 → 명희의 장기·생애 재무 해석 순으로 결합한다. 요청에 필요하지 않은 도구를 전부 호출하지 않는다. World Memory의 과거 가설, 뉴스의 현재 사건, 포트폴리오 스킬의 수치·계산은 서로 다른 증거 역할이며 충돌을 평균내지 않는다.

