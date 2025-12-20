---
layout: post
title: OpenVPN iOS앱 사용법
date: 2024-05-17T13:54:02+09:00
author: 수수
tags: ["OpenVPN", "iOS"]
categories: ["How-To"]
cover-img: /assets/posts/how_to_use_ios_openvpn_app/openvpn_0.png
thumbnail-img: /assets/posts/how_to_use_ios_openvpn_app/openvpn_0_thumb.png
subtitle: OpenVPN iOS앱 사용법을 설명합니다.
---

### 개요 
안녕하세요. 수수입니다. <br />
오늘은 OpenVPN iOS용 앱에서 ovpn파일을 로드하는 방법을 정리해보겠습니다.<br />

### OpenVPN 설명
- OpenVPN은 멀리 있는 네트워크망에 터널을 만들어 직접 통신할 수 있게하는 용도의 앱입니다.
- 일반적으로 외부에서 집/사무실 등 내부 네트워크에 안전하게 접속하여야 하는 경우에 사용됩니다.

### OpenVPN iOS앱 사용법 

#### 0. OpenVPN 앱을 설치합니다. 
- Appstore 주소: https://apps.apple.com/kr/app/openvpn-connect-openvpn-app/id590379981

#### 1. 제공받은 client.ovpn 파일을 다운받습니다.
#### 2. client.ovpn파일을 오픈한 뒤 아래쪽에 공유 버튼을 누릅니다. 
#### 3. 공유버튼을 누른 뒤 보여지는 앱 중에 설치했던 OpenVPN 앱을 찾아서 선택합니다.
![OpenVPN 1]({{ "/assets/posts/how_to_use_ios_openvpn_app/openvpn_1.jpg" | relative_url }}){:width="45%"} ![OpenVPN 2]({{ "/assets/posts/how_to_use_ios_openvpn_app/openvpn_2.jpg" | relative_url }}){:width="45%"}

#### 4. OpenVPN 앱이 오픈되며 ovpn파일을 import할지 물어봅니다. ADD 를 누릅니다.
#### 5. 네트워크 제공자에게 전달받은 id와 비밀번호를 입력하고 connect 버튼을 누릅니다.
![OpenVPN 3]({{ "/assets/posts/how_to_use_ios_openvpn_app/openvpn_3.jpg" | relative_url }}){:width="45%"} ![OpenVPN 4]({{ "/assets/posts/how_to_use_ios_openvpn_app/openvpn_4.jpg" | relative_url }}){:width="45%"}

#### 6. 접속에 성공하게 되면 아래 페이지가 보여지게 되며 앞으로는 토글 버튼을 통해 접속을 지정할 수 있습니다.
![OpenVPN 5]({{ "/assets/posts/how_to_use_ios_openvpn_app/openvpn_5.jpg" | relative_url }}){:width="45%"}
