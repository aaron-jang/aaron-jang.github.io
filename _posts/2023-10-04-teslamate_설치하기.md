---
layout: post
title: Teslamate 설치하기
subtitle: Docker를 활용한 테슬라 차량 데이터 로깅 서비스 설치 완벽 가이드
date: 2023-10-04T23:43:45+09:00
lastmod: 2025-12-28T00:00:00+09:00
author: 수수
tags: ["테슬라", "teslamate", "docker"]
categories: ["tesla"]
cover-img: /assets/images/teslamate/title.png
thumbnail-img: /assets/images/teslamate/title_thumb.png
---

### 개요

안녕하세요. 수수입니다. <br />
오늘은 docker를 통한 teslamate 설치 방법에 대해 알아보겠습니다.

### 용어 정의
- teslamate: 테슬라 차량과 관련된 데이터를 로깅할 수 있는 웹기반의 서비스
- docker: 컴퓨터 프로그램을 패키지로 싸서 어디서든 쉽게 실행할 수 있게 만들어주는 도구와 기술
- docker-compose: 여러 개의 작은 프로그램을 함께 사용해야 할 때, docker-compose는 이들을 손쉽게 묶어주는 역할을 함.

### teslamate에서 확인할 수 있는 정보
![]({{ "/assets/images/teslamate/teslamate_2.png" | relative_url }})
- 충전정보
- 충전과 관련된 이력
- 운전과 관련된 이력
- 효율성
- 위치
- 마일리지
- 예상 주행 거리 추척
- 타임라인
- 여행
- 차량 업데이트 정보
- 배터리 소진정보
- 방문한 곳 정보
### 선작업
- teslamate를 설치할 컴퓨터에 docker를 설치합니다. [링크](https://www.docker.com/products/docker-desktop/)를 통해 본인 환경에 맞게 설치하면 됩니다.

### teslamate 설치

#### docker-compose.yml 설정

아래 파일 내용을 복사하여 `docker-compose.yml` 파일 명으로 저장합니다. <br />
내용 중 값을 채워야하는 곳에는 원하는 값을 입력합니다. 입력해야하는 값은 총 두가지 입니다.
1. ENCRYPTION_KEY: Tesla API토큰을 암호화하는데 사용할 보안 암호화 키입니다.
2. DATABASE_PASS, POSTGRES_PASSWORD: 데이터베이스 비밀번호로 넣을 값입니다.

```yaml {linenos=true}
version: "3"

services:
  teslamate:
    image: teslamate/teslamate:latest
    restart: always
    environment:
      - ENCRYPTION_KEY= # 암호화키값
      - DATABASE_USER=teslamate
      - DATABASE_PASS= # DB비밀번호
      - DATABASE_NAME=teslamate
      - DATABASE_HOST=database
      - MQTT_HOST=mosquitto
    ports:
      - 4000:4000
    volumes:
      - ./import:/opt/app/import
    cap_drop:
      - all

  database:
    image: postgres:15
    restart: always
    environment:
      - POSTGRES_USER=teslamate
      - POSTGRES_PASSWORD= # DB비밀번호
      - POSTGRES_DB=teslamate
    volumes:
      - teslamate-db:/var/lib/postgresql/data

  grafana:
    image: teslamate/grafana:latest
    restart: always
    environment:
      - DATABASE_USER=teslamate
      - DATABASE_PASS= # DB비밀번호
      - DATABASE_NAME=teslamate
      - DATABASE_HOST=database
    ports:
      - 3000:3000
    volumes:
      - teslamate-grafana-data:/var/lib/grafana

  mosquitto:
    image: eclipse-mosquitto:2
    restart: always
    command: mosquitto -c /mosquitto-no-auth.conf
    # ports:
    #   - 1883:1883
    volumes:
      - mosquitto-conf:/mosquitto/config
      - mosquitto-data:/mosquitto/data

volumes:
  teslamate-db:
  teslamate-grafana-data:
  mosquitto-conf:
  mosquitto-data:
```

위 설정 내용에 보면 총 4개의 컴퓨터 프로그램을 설정하게 됩니다.
1. teslamate: teslamate의 기본 접속 프로그램
2. database: 데이터 저장소 (postgresql)
3. grafana: 데이터 저장소에 저장되어 있는 값을 시각화하여 차트와 그래프로 보여주는 용도의 프로그램
4. mosquitto: tesla 서버로부터 데이터를 수집하는 용도의 프로그램 

#### 설정한 docker-compose.yml로 teslamate 띄우기

1. docker-compose.yml을 저장한 위치로 이동하여 터미널을 실행합니다.
> **windows**: 실행 > 'cmd' 엔터 <br /> 
> **macOS, Linux**: terminal 실행
2. docker-compose 명령을 실행한다.
```
$ docker compose up -d
```
3. 여기까지하면 teslamate 설치는 완료가 된겁니다.

### teslamate 접속하기 

1. 웹브라우저를 실행하세요.
2. http://your-ip-address:4000 페이지에 접속하세요.
3. Tesla 계정으로 로그인 하세요. <br />로그인을 성공적으로 하였다면 아래와 같은 화면을 보실 수 있습니다.
![]({{ "/assets/images/teslamate/teslamate_1.png" | relative_url }})

4. 대시보드에서 메뉴를 선택하면 grafana의 웹페이지가 열립니다. (사용자: `admin`, 초기암호: `admin`)
![예시 - teslamate overview 화면]({{ "/assets/images/teslamate/teslamate_3.png" | relative_url }})

### 참고자료
- teslamate 공식 홈페이지: https://docs.teslamate.org
- teslamate 스크린샷: https://docs.teslamate.org/docs/screenshots/
- docker 공식 홈페이지: https://www.docker.com/