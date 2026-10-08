#!/usr/bin/env python3
"""디즈니 어드벤처호 층별 시설 가이드 정적 페이지 생성기.

출력: disney-adventure-decks/
  index.html          언어 선택(브라우저 언어로 자동 이동, hreflang x-default)
  {ko,en,ja,zh}/index.html  언어별 완전 렌더링된 페이지 (SEO·AI 추출용 정적 HTML)
  assets/style.css, assets/app.js  공통 자원

데이터·번역을 이 파일에서만 관리하고, 수정 후 `python3 scripts/build-disney-guide.py` 로 재생성한다.
"""
import json, os, html, datetime

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "disney-adventure-decks")
SITE = "https://soosoo.life"
BASE = "/disney-adventure-decks"
UPDATED = "2026-10-08"
LANGS = ["ko", "en", "ja", "zh-cn", "zh-tw"]
HREFLANG = {"ko": "ko", "en": "en", "ja": "ja", "zh-cn": "zh-Hans", "zh-tw": "zh-Hant"}
LANG_NAME = {"ko": "한국어", "en": "English", "ja": "日本語", "zh-cn": "简体中文", "zh-tw": "繁體中文"}
OG_LOCALE = {"ko": "ko_KR", "en": "en_US", "ja": "ja_JP", "zh-cn": "zh_CN", "zh-tw": "zh_TW"}
# 데이터는 간체(zh)로 작성하고, 번체(zh-tw)는 OpenCC(s2twp)로 변환 + 대만 용어 보정
DATA_KEY = {"ko": "ko", "en": "en", "ja": "ja", "zh-cn": "zh", "zh-tw": "zh"}
TW_FIX = {"過山車": "雲霄飛車", "無邊泳池": "無邊際泳池", "KTV包間": "KTV包廂", "影院": "電影院",
          "幼兒戲水池": "幼兒戲水區", "托兒所": "托嬰中心"}
try:
    from opencc import OpenCC
    _cc = OpenCC("s2twp")
except ImportError:
    raise SystemExit("opencc 가 필요합니다: pip3 install --break-system-packages opencc-python-reimplemented")
def to_tw(x):
    if isinstance(x, str):
        y = _cc.convert(x)
        for a, b in TW_FIX.items(): y = y.replace(a, b)
        return y
    if isinstance(x, list): return [to_tw(i) for i in x]
    if isinstance(x, tuple): return tuple(to_tw(i) for i in x)
    if isinstance(x, dict): return {k: to_tw(v) for k, v in x.items()}
    return x
def tr(d, L):
    """언어별 문자열 dict 에서 L 에 맞는 값 (zh-tw 는 zh 를 번체로 변환)"""
    k = DATA_KEY[L]
    return to_tw(d[k]) if L == "zh-tw" else d[k]

# ---------------------------------------------------------------- UI 문자열
UI = {
 "ko": dict(
  title="디즈니 어드벤처호 층별 시설 가이드", h1="디즈니 어드벤처호<br>층별 공용 시설 가이드",
  sub="싱가포르 모항 디즈니 크루즈. 층을 누르면 바로 이동하고, 카테고리나 이름으로 원하는 시설만 골라볼 수 있어요.",
  desc="싱가포르 모항 디즈니 크루즈 '디즈니 어드벤처'의 5~19층 공용 시설을 층별·카테고리별로 정리한 가이드. 메인 다이닝 6곳, 뷔페, 수영장, 키즈클럽, 영화관, 유료 시설, 컨시어지 전용 구역까지 한눈에.",
  facts=[("승객 층","19개","(14층 없음)"),("테마 구역","7곳",""),("키즈클럽","3~10세","· 틴 11~17세"),("첫 출항","2026.3.10","")],
  search_label="시설 이름 검색", search_ph="시설 이름 검색 (예: 수영장, Palo, 커피)", filter_label="카테고리 필터",
  all="전체", paid_chip="유료 식음료", movie_chip="영화", main_chip="메인 다이닝", buffet_chip="뷔페",
  ship_nav="층 바로가기", ship_label="선박 단면 · 위가 최상층", hull="1–4층 · 승무원 전용",
  none="조건에 맞는 시설이 없어요. 검색어를 지우거나 다른 카테고리를 골라보세요.", result="{n}개 시설이 보여요",
  deck_unit="층", deck_aria="{n}층 ", concierge_only="(일반 승객 이용 불가)",
  lbl_main="메인 다이닝", lbl_buffet="뷔페 (아침·점심)", lbl_cinema="영화관 (4개관)", lbl_screen="야외 대형 스크린",
  lbl_paid="유료", lbl_partpaid="일부 유료", lbl_lock="컨시어지", theme="테마", theme_aria="화면 테마 바꾸기",
  notes_aria="참고 사항", lang_label="언어", back="← 수수라이프 블로그", updated="업데이트",
  notes=[
   ('🔒 컨시어지','표시·취소선 시설은 컨시어지 객실 투숙객 전용이에요.'),
   ('🍽️ 메인 다이닝','은 저녁마다 식당을 바꿔 가며 먹는 로테이션 식당 6곳(크루즈 요금 포함)이고, 🍱 뷔페 2곳은 아침·점심에만 뷔페로 운영돼요.'),
   ('💰 유료','는 추가 요금이 붙는 곳, 💰 일부 유료는 기본 음료는 무료지만 스페셜티 음료가 유료인 곳이에요. 일반 커피·차·탄산음료·주스는 무료, 바·라운지 음료는 유료예요.'),
   ('🕒 운영 시간',"은 항해일마다 달라 승선 후 Navigator 앱에만 표시돼요. 여기 적은 시간은 공개 자료로 확인된 것만이에요. 룸서비스는 24시간 무료예요."),
   ('출처','공식 덱플랜 기반 자료(WDW News Today 2026.3, Cruise Critic, CruiseMapper). 운영 중 변경될 수 있으니 승선 후 Navigator 앱으로 확인하세요.'),
  ],
  decks_fmt="{n}층", cabins="객실", no_public="승객 시설 없음", cabins_laundry="객실 · 세탁실", cabins_medical="객실 · 의료센터",
 ),
 "en": dict(
  title="Disney Adventure Deck-by-Deck Guide", h1="Disney Adventure<br>Deck-by-Deck Venue Guide",
  sub="Disney Cruise Line's Singapore-based ship. Tap a deck to jump to it, or filter venues by category or name.",
  desc="A deck-by-deck guide to the public venues on Disney Adventure, Disney Cruise Line's Singapore-homeported ship (Decks 5–19): six rotational dining restaurants, buffets, pools, kids clubs, cinemas, extra-charge venues and concierge-only areas.",
  facts=[("Passenger decks","19","(no Deck 14)"),("Themed areas","7",""),("Kids club","ages 3–10","· teens 11–17"),("Maiden voyage","Mar 10, 2026","")],
  search_label="Search venues", search_ph="Search venues (e.g. pool, Palo, coffee)", filter_label="Category filter",
  all="All", paid_chip="Extra charge", movie_chip="Movies", main_chip="Main dining", buffet_chip="Buffet",
  ship_nav="Jump to deck", ship_label="Ship cross-section · top deck first", hull="Decks 1–4 · crew only",
  none="No venues match. Clear the search or pick another category.", result="{n} venues shown",
  deck_unit="", deck_aria="Deck {n}: ", concierge_only="(not available to regular guests)",
  lbl_main="Main dining", lbl_buffet="Buffet (breakfast & lunch)", lbl_cinema="Cinema (4 screens)", lbl_screen="Outdoor big screen",
  lbl_paid="Extra charge", lbl_partpaid="Partly extra", lbl_lock="Concierge", theme="Theme", theme_aria="Toggle color theme",
  notes_aria="Notes", lang_label="Language", back="← Soosoo Life blog", updated="Updated",
  notes=[
   ('🔒 Concierge','-tagged venues with a strikethrough are reserved for concierge stateroom guests.'),
   ('🍽️ Main dining','means the six rotational restaurants you cycle through each evening (included in the fare). The two 🍱 buffet venues run as buffets at breakfast and lunch only.'),
   ('💰 Extra charge','marks venues that cost extra; 💰 Partly extra means basic drinks are free but specialty drinks cost extra. Regular coffee, tea, soft drinks and juice are free; drinks at bars and lounges cost extra.'),
   ('🕒 Hours',"vary by sailing day and are published only in the Navigator app once on board. Only times confirmed by public sources are listed here. Room service is free around the clock."),
   ('Sources','Based on the official deck plans (WDW News Today, Mar 2026; Cruise Critic; CruiseMapper). Subject to change — confirm in the Navigator app once on board.'),
  ],
  decks_fmt="Decks {n}", cabins="Staterooms", no_public="No public venues", cabins_laundry="Staterooms · Laundry", cabins_medical="Staterooms · Medical Center",
 ),
 "ja": dict(
  title="ディズニー・アドベンチャー デッキ別施設ガイド", h1="ディズニー・アドベンチャー<br>デッキ別パブリック施設ガイド",
  sub="シンガポール母港のディズニークルーズ。デッキをタップすると移動し、カテゴリーや名前で施設を絞り込めます。",
  desc="シンガポールを母港とするディズニークルーズ「ディズニー・アドベンチャー」の5〜19階パブリック施設をデッキ別・カテゴリー別に整理したガイド。ローテーションダイニング6か所、ビュッフェ、プール、キッズクラブ、映画館、有料施設、コンシェルジュ専用エリアまで一目で。",
  facts=[("乗客デッキ","19層","(14階なし)"),("テーマエリア","7か所",""),("キッズクラブ","3〜10歳","· ティーン 11〜17歳"),("初航海","2026.3.10","")],
  search_label="施設名で検索", search_ph="施設名で検索（例：プール、Palo、コーヒー）", filter_label="カテゴリーフィルター",
  all="すべて", paid_chip="有料の飲食", movie_chip="映画", main_chip="メインダイニング", buffet_chip="ビュッフェ",
  ship_nav="デッキへ移動", ship_label="船体断面 · 上が最上階", hull="1〜4階 · クルー専用",
  none="条件に合う施設がありません。検索語を消すか、別のカテゴリーを選んでください。", result="{n}件の施設を表示中",
  deck_unit="階", deck_aria="{n}階 ", concierge_only="（一般の乗客は利用不可）",
  lbl_main="メインダイニング", lbl_buffet="ビュッフェ（朝・昼）", lbl_cinema="映画館（4スクリーン）", lbl_screen="屋外大型スクリーン",
  lbl_paid="有料", lbl_partpaid="一部有料", lbl_lock="コンシェルジュ", theme="テーマ", theme_aria="画面テーマを切り替え",
  notes_aria="注意事項", lang_label="言語", back="← Soosoo Life ブログ", updated="更新",
  notes=[
   ('🔒 コンシェルジュ','表示・取り消し線の施設はコンシェルジュ客室の宿泊者専用です。'),
   ('🍽️ メインダイニング','は毎晩レストランを変えて食事するローテーション式レストラン6か所（クルーズ料金込み）、🍱 ビュッフェ2か所は朝食・昼食のみビュッフェとして営業します。'),
   ('💰 有料','は追加料金がかかる施設、💰 一部有料は基本ドリンクは無料でスペシャルティドリンクが有料の施設です。通常のコーヒー・紅茶・ソフトドリンク・ジュースは無料、バー・ラウンジのドリンクは有料です。'),
   ('🕒 営業時間','は航海日によって異なり、乗船後の Navigator アプリにのみ表示されます。ここに記載の時間は公開資料で確認できたもののみです。ルームサービスは24時間無料です。'),
   ('出典','公式デッキプラン準拠の資料（WDW News Today 2026年3月、Cruise Critic、CruiseMapper）。運航中に変更される場合があるため、乗船後に Navigator アプリで確認してください。'),
  ],
  decks_fmt="{n}階", cabins="客室", no_public="乗客用施設なし", cabins_laundry="客室 · ランドリー", cabins_medical="客室 · メディカルセンター",
 ),
 "zh": dict(
  title="迪士尼冒险号 分层设施指南", h1="迪士尼冒险号<br>分层公共设施指南",
  sub="以新加坡为母港的迪士尼邮轮。点击楼层即可跳转，也可按类别或名称筛选设施。",
  desc="以新加坡为母港的迪士尼邮轮“迪士尼冒险号”5至19层公共设施分层、分类整理指南：6家轮换主餐厅、自助餐、泳池、儿童俱乐部、影院、收费设施及礼宾专属区域一目了然。",
  facts=[("乘客楼层","19层","(无14层)"),("主题区域","7个",""),("儿童俱乐部","3~10岁","· 青少年 11~17岁"),("首航","2026.3.10","")],
  search_label="搜索设施名称", search_ph="搜索设施名称（如：泳池、Palo、咖啡）", filter_label="类别筛选",
  all="全部", paid_chip="收费餐饮", movie_chip="电影", main_chip="主餐厅", buffet_chip="自助餐",
  ship_nav="跳转楼层", ship_label="船体剖面 · 顶层在上", hull="1–4层 · 船员专用",
  none="没有符合条件的设施。请清除搜索词或选择其他类别。", result="显示 {n} 个设施",
  deck_unit="层", deck_aria="{n}层 ", concierge_only="（普通乘客不可使用）",
  lbl_main="主餐厅", lbl_buffet="自助餐（早·午）", lbl_cinema="影院（4个厅）", lbl_screen="户外大屏幕",
  lbl_paid="收费", lbl_partpaid="部分收费", lbl_lock="礼宾", theme="主题", theme_aria="切换界面主题",
  notes_aria="注意事项", lang_label="语言", back="← Soosoo Life 博客", updated="更新",
  notes=[
   ('🔒 礼宾','标记并带删除线的设施仅限礼宾客房住客使用。'),
   ('🍽️ 主餐厅','指每晚轮换就餐的6家轮换餐厅（含在船票内），🍱 自助餐2处仅在早餐、午餐时段以自助形式运营。'),
   ('💰 收费','指需额外付费的设施，💰 部分收费指基础饮品免费但特色饮品收费。普通咖啡、茶、碳酸饮料和果汁免费，酒吧、酒廊饮品收费。'),
   ('🕒 营业时间','因航行日而异，仅在登船后的 Navigator 应用中显示。此处仅列出公开资料可确认的时间。客房送餐 24 小时免费。'),
   ('来源','基于官方甲板图的资料（WDW News Today 2026年3月、Cruise Critic、CruiseMapper）。运营期间可能变更，请登船后在 Navigator 应用中确认。'),
  ],
  decks_fmt="{n}层", cabins="客房", no_public="无乘客设施", cabins_laundry="客房 · 洗衣房", cabins_medical="客房 · 医疗中心",
 ),
}

# ---------------------------------------------------------------- 카테고리
CATS = {
 "dining":{"e":"🍽️","ko":"식사","en":"Dining","ja":"食事","zh":"餐饮"},
 "cafe":{"e":"☕","ko":"카페·간식","en":"Café & snacks","ja":"カフェ・軽食","zh":"咖啡·小吃"},
 "bar":{"e":"🍸","ko":"바·라운지","en":"Bars & lounges","ja":"バー・ラウンジ","zh":"酒吧·酒廊"},
 "show":{"e":"🎭","ko":"공연·엔터","en":"Shows & entertainment","ja":"ショー・エンタメ","zh":"演出·娱乐"},
 "kids":{"e":"🧒","ko":"키즈·틴","en":"Kids & teens","ja":"キッズ・ティーン","zh":"儿童·青少年"},
 "pool":{"e":"🌊","ko":"물놀이","en":"Pools & water play","ja":"プール・水遊び","zh":"戏水"},
 "ride":{"e":"🎢","ko":"어트랙션","en":"Attractions","ja":"アトラクション","zh":"游乐设施"},
 "shop":{"e":"🛍️","ko":"쇼핑","en":"Shopping","ja":"ショッピング","zh":"购物"},
 "well":{"e":"💆","ko":"스파·운동","en":"Spa & fitness","ja":"スパ・フィットネス","zh":"水疗·健身"},
 "svc":{"e":"🛎️","ko":"서비스","en":"Services","ja":"サービス","zh":"服务"},
 "space":{"e":"📍","ko":"테마 광장","en":"Themed area","ja":"テーマ広場","zh":"主题广场"},
 "etc":{"e":"✨","ko":"기타","en":"Other","ja":"その他","zh":"其他"},
}
SYN = {"dining":"식당 레스토랑 밥 음식 restaurant food レストラン 餐厅","cafe":"커피 카페 티 차 음료 디저트 coffee tea cafe コーヒー 咖啡","bar":"술 칵테일 맥주 와인 바 cocktail beer wine バー 酒吧","show":"공연 쇼 영화 게임 show movie theatre ショー 演出","kids":"아이 어린이 키즈 틴 kids teens 子供 儿童","pool":"수영장 풀 물놀이 슬라이드 pool slide プール 泳池","ride":"놀이기구 롤러코스터 ride coaster アトラクション 游乐","shop":"쇼핑 기념품 매장 shop store ショップ 商店","well":"스파 헬스 운동 마사지 spa gym fitness スパ 水疗","svc":"서비스 service サービス 服务","space":"광장 구역 area plaza 広場 广场","etc":""}
CHIP_ORDER = ["all","dining","buffet","main","pool","kids","ride","movie","show","cafe","paid","bar","shop","well","svc","space","etc"]

def T(ko,en,ja,zh): return {"ko":ko,"en":en,"ja":ja,"zh":zh}
E = T("","","","")

# ---------------------------------------------------------------- 층 데이터
# venue: (영문 이름, 설명{lang}, 카테고리, 컨시어지 전용)
DECKS = [
 {"n":"20","t":"no_public","cab":True,"v":[]},
 {"n":"19","t":T("Marvel Landing 상층 · 컨시어지 선덱","Marvel Landing (upper) · Concierge sun deck","Marvel Landing 上層 · コンシェルジュ サンデッキ","Marvel Landing 上层 · 礼宾日光甲板"),
  "d":T("롤러코스터와 슬라이드 출발점, 컨시어지 전용 선덱.","Start of the roller coaster and slide, plus the concierge-only sun deck.","ローラーコースターとスライダーの出発点、コンシェルジュ専用サンデッキ。","过山车和滑梯的起点，以及礼宾专属日光甲板。"),
  "v":[
   ("Ironcycle Test Run",T("디즈니 크루즈 최초 롤러코스터 (약 250m)","First roller coaster on a Disney ship (about 250 m)","ディズニークルーズ初のローラーコースター（約250m）","迪士尼邮轮首座过山车（约250米）"),"ride",0),
   ("Woody & Jessie's Wild Slide",T("워터슬라이드","Water slide","ウォータースライダー","水上滑梯"),"pool",0),
   ("Concierge Sundeck & Pool",T("컨시어지 선덱·수영장","Concierge sun deck & pool","コンシェルジュ サンデッキ・プール","礼宾日光甲板·泳池"),"pool",1),
   ("Concierge Sundeck Dining",T("컨시어지 선덱 다이닝","Concierge sun deck dining","コンシェルジュ サンデッキ ダイニング","礼宾日光甲板餐饮"),"dining",1)]},
 {"n":"18","t":T("Marvel Landing","Marvel Landing","Marvel Landing","Marvel Landing"),
  "d":T("마블 놀이기구, 인피니티 풀, 러닝 트랙.","Marvel rides, the infinity pool and the running track.","マーベルのアトラクション、インフィニティプール、ランニングトラック。","漫威游乐设施、无边泳池和跑道。"),
  "v":[
   ("Groot Galaxy Spin",T("그루트 회전 놀이기구","Groot spinning ride","グルートの回転アトラクション","格鲁特旋转游乐设施"),"ride",0),
   ("Pym Quantum Racers",T("핌 퀀텀 레이서","Pym Quantum Racers ride","ピム・クアンタム・レーサー","皮姆量子赛车"),"ride",0),
   ("Marvel Landing",T("마블 테마 구역","Marvel-themed area","マーベル テーマエリア","漫威主题区"),"space",0),
   ("Infinity Pool",T("인피니티 풀","Infinity pool","インフィニティプール","无边泳池"),"pool",0),
   ("Infinity Bar",T("풀사이드 바","Poolside bar","プールサイドバー","池畔酒吧"),"bar",0),
   ("Running Track",T("러닝 트랙","Running track","ランニングトラック","跑道"),"well",0),
   ("Opulence Spa – Elemis at Sea",T("컨시어지 스파","Concierge spa","コンシェルジュ スパ","礼宾水疗"),"well",1),
   ("Concierge Fitness Center",T("컨시어지 피트니스","Concierge fitness center","コンシェルジュ フィットネス","礼宾健身中心"),"well",1)]},
 {"n":"17","t":T("Toy Story Place · 메인 풀덱","Toy Story Place · Main pool deck","Toy Story Place · メインプールデッキ","Toy Story Place · 主泳池甲板"),
  "d":T("가족 수영장·슬라이드·뷔페가 모인 가장 붐비는 야외층.","The busiest outdoor deck: family pool, slides and the buffet.","ファミリープール・スライダー・ビュッフェが集まる、最もにぎわう屋外デッキ。","家庭泳池、滑梯和自助餐齐聚，最热闹的户外楼层。"),
  "v":[
   ("Sunnyside Pool",T("가족 수영장","Family pool","ファミリープール","家庭泳池"),"pool",0),
   ("Woody & Jessie's Wild Slides",T("워터슬라이드","Water slides","ウォータースライダー","水上滑梯"),"pool",0),
   ("Flying Saucer Splash Zone",T("어린이 물놀이존","Kids' splash zone","子ども向け水遊びゾーン","儿童戏水区"),"pool",0),
   ("Toy Story Splash Pad",T("유아 스플래시 패드","Toddler splash pad","幼児用スプラッシュパッド","幼儿戏水池"),"pool",0),
   ("Pixar Market Restaurant",T("아침·점심 뷔페, 저녁은 메인 다이닝","Buffet at breakfast & lunch, main dining at dinner","朝・昼はビュッフェ、夜はメインダイニング","早午自助餐，晚餐为主餐厅"),"dining",0),
   ("Pizza Planet",T("피자","Pizza","ピザ","披萨"),"dining",0),
   ("Wheezy's Freezies",T("아이스크림·프로즌","Ice cream & frozen treats","アイスクリーム・フローズン","冰淇淋·冷饮"),"cafe",0),
   ("Market Bar",T("바","Bar","バー","酒吧"),"bar",0),
   ("Bounce and Hops",E,"etc",0),
   ("Toy Story Place Seating Area",T("대형 스크린 2개로 낮 동안 영화 상영","Two big screens showing movies during the day","大型スクリーン2面で日中に映画を上映","两块大屏幕白天放映电影"),"space",0),
   ("Palace Treasures",E,"shop",0),
   ("3 Wishes",E,"etc",0),
   ("Concierge Lounge",T("컨시어지 라운지","Concierge lounge","コンシェルジュ ラウンジ","礼宾酒廊"),"bar",1)]},
 {"n":"16","t":"cabins_laundry","v":[("Fairytale Fresh Laundry",T("셀프 세탁실","Self-service laundry","セルフランドリー","自助洗衣房"),"svc",0)]},
 {"n":"15","t":"cabins","cab":True,"v":[]},
 {"n":"13","t":"cabins","cab":True,"v":[]},
 {"n":"12","t":"cabins","cab":True,"v":[]},
 {"n":"11","t":T("Imagination Garden 상층","Imagination Garden (upper)","Imagination Garden 上層","Imagination Garden 上层"),
  "d":T("10층 광장을 내려다보는 바와 숍.","Bars and a shop overlooking the Deck 10 plaza.","10階の広場を見下ろすバーとショップ。","俯瞰10层广场的酒吧和商店。"),
  "v":[
   ("Disney Imagination Garden",T("가든 광장 (상층)","Garden plaza (upper level)","ガーデン広場（上層）","花园广场（上层）"),"space",0),
   ("Disney Discovery Reef",T("디스커버리 리프 구역","Discovery Reef area","ディスカバリーリーフ エリア","探索礁区"),"space",0),
   ("Wayfinder Bay",T("모아나 테마 구역","Moana-themed area","モアナ テーマエリア","海洋奇缘主题区"),"space",0),
   ("Garden Bar",T("가든 바","Garden bar","ガーデンバー","花园酒吧"),"bar",0),
   ("Taverna Portorosso",T("루카 테마 바","Luca-themed bar","『あの夏のルカ』テーマのバー","夏日友晴天主题酒吧"),"bar",0),
   ("Palo Trattoria",T("성인 전용 이탈리안 (상층)","Adults-only Italian (upper level)","大人専用イタリアン（上層）","成人专属意大利餐厅（上层）"),"dining",0),
   ("Castle Collection",T("기념품숍","Gift shop","ギフトショップ","纪念品店"),"shop",0)]},
 {"n":"10","t":T("Imagination Garden · 캐주얼 푸드 허브","Imagination Garden · Casual food hub","Imagination Garden · カジュアルフードハブ","Imagination Garden · 休闲美食中心"),
  "d":T("배의 중심 야외 광장. 캐주얼 식당, 스파·헬스가 모여 있어요.","The ship's central outdoor plaza, with casual eateries, spa and fitness.","船の中心となる屋外広場。カジュアルレストラン、スパ・フィットネスが集まります。","船的中心户外广场，汇集休闲餐厅、水疗和健身。"),
  "v":[
   ("Disney Imagination Garden",T("스토리북 캐슬이 있는 중앙 광장","Central plaza with the Storybook Castle","ストーリーブック・キャッスルのある中央広場","设有故事书城堡的中央广场"),"space",0),
   ("Garden Stage",T("야외 공연 무대","Outdoor stage","屋外ステージ","户外舞台"),"show",0),
   ("Disney Discovery Reef",T("디스커버리 리프 구역","Discovery Reef area","ディスカバリーリーフ エリア","探索礁区"),"space",0),
   ("Wayfinder Bay",T("모아나 테마 구역","Moana-themed area","モアナ テーマエリア","海洋奇缘主题区"),"space",0),
   ("Mike & Sulley's Flavors of Asia",T("아시안 캐주얼","Casual Asian","アジアンカジュアル","亚洲休闲餐"),"dining",0),
   ("Stitch's 'Ohana Grill",T("그릴","Grill","グリル","烧烤"),"dining",0),
   ("Mowgli's Eatery",T("캐주얼 식당","Casual eatery","カジュアルレストラン","休闲餐厅"),"dining",0),
   ("Gramma Tala's Kitchen",T("캐주얼 식당","Casual eatery","カジュアルレストラン","休闲餐厅"),"dining",0),
   ("Cosmic Kebabs",T("케밥","Kebabs","ケバブ","烤肉串"),"dining",0),
   ("Palo Trattoria",T("성인 전용 이탈리안","Adults-only Italian","大人専用イタリアン","成人专属意大利餐厅"),"dining",0),
   ("Palo Cafe",T("카페","Café","カフェ","咖啡馆"),"cafe",0),
   ("Bewitching Boba & Brews",T("버블티·음료","Bubble tea & drinks","タピオカ・ドリンク","珍珠奶茶·饮品"),"cafe",0),
   ("Wayfinder Bar",T("바","Bar","バー","酒吧"),"bar",0),
   ("Treasures Untold",T("숍","Shop","ショップ","商店"),"shop",0),
   ("Infinite Bliss Spa – Elemis at Sea",T("스파","Spa","スパ","水疗"),"well",0),
   ("Fitness Center",T("피트니스 센터","Fitness center","フィットネスセンター","健身中心"),"well",0),
   ("Prayer Room",T("기도실","Prayer room","祈祷室","祈祷室"),"svc",0)]},
 {"n":"9","t":"cabins_medical","v":[
   ("Animator's Table Restaurant",T("메인 다이닝","Main dining","メインダイニング","主餐厅"),"dining",0),
   ("Medical Center",T("의료센터","Medical center","メディカルセンター","医疗中心"),"svc",0)]},
 {"n":"8","t":T("키즈 층","Kids deck","キッズフロア","儿童楼层"),
  "d":T("영유아 너서리부터 3~10세 키즈클럽까지 한 층에.","Nursery for little ones and the kids club for ages 3–10, all on one deck.","乳幼児向けナーサリーから3〜10歳のキッズクラブまでワンフロアに。","从婴幼儿托儿所到3~10岁儿童俱乐部，集中在同一层。"),
  "v":[
   ("Disney's Oceaneer Club",T("키즈클럽 (3~10세)","Kids club (ages 3–10)","キッズクラブ（3〜10歳）","儿童俱乐部（3~10岁）"),"kids",0),
   ("\"it's a small world\" nursery",T("영유아 너서리","Nursery for babies & toddlers","乳幼児ナーサリー","婴幼儿托儿所"),"kids",0),
   ("Mickey & Minnie Captain's Deck",T("키즈클럽 구역","Kids club area","キッズクラブ エリア","儿童俱乐部区域"),"kids",0),
   ("Walt Disney Imagineering Lab",T("키즈클럽 구역","Kids club area","キッズクラブ エリア","儿童俱乐部区域"),"kids",0),
   ("Andy's Toy Box",T("키즈클럽 구역","Kids club area","キッズクラブ エリア","儿童俱乐部区域"),"kids",0),
   ("Marvel WEB Workshop",T("키즈클럽 구역","Kids club area","キッズクラブ エリア","儿童俱乐部区域"),"kids",0),
   ("Fairytale Hall",T("키즈클럽 구역","Kids club area","キッズクラブ エリア","儿童俱乐部区域"),"kids",0),
   ("Hollywood Spotlight Club",T("메인 다이닝","Main dining","メインダイニング","主餐厅"),"dining",0)]},
 {"n":"7","t":T("San Fransokyo Street","San Fransokyo Street","San Fransokyo Street","San Fransokyo Street"),
  "d":T("빅 히어로 6 테마 거리. 쇼핑·영화관·오락실·틴 클럽.","Big Hero 6-themed street: shopping, cinemas, arcade and teen clubs.","『ベイマックス』テーマのストリート。ショッピング・映画館・ゲームセンター・ティーンクラブ。","超能陆战队主题街区：购物、影院、游戏厅和青少年俱乐部。"),
  "v":[
   ("San Fransokyo Street",T("빅 히어로 6 테마 거리","Big Hero 6-themed street","『ベイマックス』テーマのストリート","超能陆战队主题街区"),"space",0),
   ("Walt Disney Theatre",T("메인 공연장 (상층)","Main theatre (upper level)","メインシアター（上層）","主剧院（上层）"),"show",0),
   ("Baymax Cinemas",T("디즈니·픽사·마블·루카스필름 개봉작 상영","Disney, Pixar, Marvel and Lucasfilm releases","ディズニー・ピクサー・マーベル・ルーカスフィルムの新作を上映","放映迪士尼、皮克斯、漫威、卢卡斯影业新片"),"show",0),
   ("Big Hero Arcade",T("오락실","Arcade","ゲームセンター","游戏厅"),"show",0),
   ("Private Karaoke Rooms",T("프라이빗 노래방","Private karaoke rooms","プライベートカラオケ","私人KTV包间"),"show",0),
   ("D Lounge",T("가족 라운지","Family lounge","ファミリーラウンジ","家庭酒廊"),"show",0),
   ("Edge",T("틴 클럽 (11~14세)","Tween club (ages 11–14)","ティーンクラブ（11〜14歳）","青少年俱乐部（11~14岁）"),"kids",0),
   ("Vibe",T("틴 클럽 (14~17세)","Teen club (ages 14–17)","ティーンクラブ（14〜17歳）","青少年俱乐部（14~17岁）"),"kids",0),
   ("Bibbidi Bobbidi Boutique",T("어린이 변신 살롱","Kids' makeover salon","子ども向け変身サロン","儿童变装沙龙"),"kids",0),
   ("Royal Studio",E,"etc",0),
   ("Bacha Coffee",T("커피","Coffee","コーヒー","咖啡"),"cafe",0),
   ("TWG Tea",T("티 하우스","Tea house","ティーハウス","茶馆"),"cafe",0),
   ("Alley Cat Cafe",T("카페","Café","カフェ","咖啡馆"),"cafe",0),
   ("Duffy and Friends Shop",T("더피 기념품","Duffy merchandise","ダッフィーグッズ","达菲周边"),"shop",0),
   ("National Geographic Shop",T("내셔널 지오그래픽 숍","National Geographic shop","ナショナル ジオグラフィック ショップ","国家地理商店"),"shop",0),
   ("Diamonds and Wishes",T("주얼리","Jewelry","ジュエリー","珠宝"),"shop",0),
   ("Pics Photo Shop",T("사진 구매","Photo purchases","写真購入","照片购买"),"shop",0),
   ("Disney Studio",E,"etc",0)]},
 {"n":"6","t":T("Town Square · 로비","Town Square · Lobby","Town Square · ロビー","Town Square · 大堂"),
  "d":T("게스트 서비스와 바·라운지, 메인 다이닝 두 곳.","Guest Services, bars and lounges, and two main dining restaurants.","ゲストサービスとバー・ラウンジ、メインダイニング2か所。","宾客服务、酒吧酒廊，以及两家主餐厅。"),
  "v":[
   ("Town Square",T("로비 광장","Lobby atrium","ロビー広場","大堂广场"),"space",0),
   ("Guest Services",T("게스트 서비스","Guest Services","ゲストサービス","宾客服务"),"svc",0),
   ("Walt Disney Theatre",T("메인 공연장","Main theatre","メインシアター","主剧院"),"show",0),
   ("Enchanted Summer Restaurant",T("아침·점심 뷔페, 저녁은 메인 다이닝","Buffet at breakfast & lunch, main dining at dinner","朝・昼はビュッフェ、夜はメインダイニング","早午自助餐，晚餐为主餐厅"),"dining",0),
   ("Navigator's Club Restaurant",T("메인 다이닝","Main dining","メインダイニング","主餐厅"),"dining",0),
   ("Premiere Sips & Snacks",T("공연장 스낵","Theatre snacks","シアター スナック","剧院小吃"),"cafe",0),
   ("Spellbound",T("바","Bar","バー","酒吧"),"bar",0),
   ("Royal Court Lounge",T("라운지","Lounge","ラウンジ","酒廊"),"bar",0),
   ("Buccaneer Bar",T("바","Bar","バー","酒吧"),"bar",0),
   ("Marvel Style Studio",T("어린이 마블 변신","Marvel makeovers for kids","子ども向けマーベル変身","儿童漫威变装"),"kids",0)]},
 {"n":"5","t":T("공연장 하층 · 쇼핑","Theatre (lower) · Shopping","シアター下層 · ショッピング","剧院下层 · 购物"),
  "d":T("승선 후 가장 아래 공용층.","The lowest public deck for guests.","乗客が利用できる最下層のパブリックデッキ。","乘客可使用的最底层公共甲板。"),
  "v":[
   ("Walt Disney Theatre",T("메인 공연장 (하층)","Main theatre (lower level)","メインシアター（下層）","主剧院（下层）"),"show",0),
   ("Animator's Palate Restaurant",T("메인 다이닝","Main dining","メインダイニング","主餐厅"),"dining",0),
   ("Tiana's Bayou Lounge",T("라운지","Lounge","ラウンジ","酒廊"),"bar",0),
   ("World of Disney",T("대형 기념품숍","Large Disney store","大型ディズニーストア","大型迪士尼商店"),"shop",0)]},
]
# 운영 시간·예약 (공개 자료에서 확인된 것만). 정확한 시간은 항해일마다 달라 Navigator 앱에만 표시됨
H_MAIN   = T("저녁 2회 좌석 17:45 / 20:15 (예약 시 배정)", "Dinner seatings 5:45 PM / 8:15 PM (assigned at booking)", "夕食2回制 17:45 / 20:15（予約時に割り当て）", "晚餐两场 17:45 / 20:15（预订时分配）")
H_BUFFET = T("아침·점심 뷔페 · 저녁 2회 좌석 17:45 / 20:15", "Breakfast & lunch buffet · dinner seatings 5:45 / 8:15 PM", "朝・昼ビュッフェ · 夕食2回制 17:45 / 20:15", "早午自助餐 · 晚餐两场 17:45 / 20:15")
HOURS = {
  "Palo Trattoria": T("저녁 전용 · 18세 이상 · 예약 필수 · 1인 $55", "Dinner only · ages 18+ · reservation required · $55 per person", "夕食のみ · 18歳以上 · 要予約 · 1人 $55", "仅晚餐 · 18岁以上 · 需预订 · 每人 $55"),
  "Mike & Sulley's Flavors of Asia": T("예약 필수 · 코스 $115~200", "Reservation required · set menus $115–200", "要予約 · コース $115〜200", "需预订 · 套餐 $115~200"),
  "Mowgli's Eatery": T("Navigator 앱에서 사전 예약 권장", "Reservation via the Navigator app recommended", "Navigator アプリでの事前予約推奨", "建议通过 Navigator 应用预订"),
  "Wheezy's Freezies": T("매일 자정까지 · 소프트아이스크림 무료", "Open until midnight daily · soft-serve is free", "毎日深夜0時まで · ソフトクリーム無料", "每日营业至午夜 · 软冰淇淋免费"),
}
def hours_for(name, L):
    if name in MAIN: return tr(H_BUFFET if name in BUFFET else H_MAIN, L)
    return tr(HOURS[name], L) if name in HOURS else ""

PAID = {"Palo Trattoria":"paid","Mike & Sulley's Flavors of Asia":"paid","Bacha Coffee":"paid","TWG Tea":"paid","Palo Cafe":"paid",
        "Spellbound":"paid","Tiana's Bayou Lounge":"paid","Buccaneer Bar":"paid","Garden Bar":"paid","Wayfinder Bar":"paid",
        "Market Bar":"paid","Infinity Bar":"paid","Taverna Portorosso":"paid","Bewitching Boba & Brews":"part","Alley Cat Cafe":"part"}
MAIN = {"Animator's Palate Restaurant","Enchanted Summer Restaurant","Navigator's Club Restaurant","Hollywood Spotlight Club","Animator's Table Restaurant","Pixar Market Restaurant"}
MOVIE = {"Baymax Cinemas":"cinema","Toy Story Place Seating Area":"screen"}
BUFFET = {"Pixar Market Restaurant","Enchanted Summer Restaurant"}

esc = lambda s: html.escape(s, quote=True)

def deck_title(dk, L):
    t = dk["t"]
    return ui_for(L)[t] if isinstance(t, str) else tr(t, L)

# ---------------------------------------------------------------- 렌더링
def ui_for(L):
    base = UI[DATA_KEY[L]]
    return to_tw(base) if L == "zh-tw" else base

def render_lang(L):
    u = ui_for(L); hl = HREFLANG[L]
    url = f"{SITE}{BASE}/{L}/"
    alternates = "\n".join(f'<link rel="alternate" hreflang="{HREFLANG[x]}" href="{SITE}{BASE}/{x}/">' for x in LANGS)
    alternates += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{BASE}/">'

    # 선박 단면 내비
    stack = []
    pending_cab = []
    def flush_cab():
        if pending_cab:
            fmt = u["decks_fmt"] if len(pending_cab) > 1 else u["decks_fmt"].replace("Decks", "Deck")
            label = f'{fmt.format(n="·".join(pending_cab))} · {u["cabins"]}'
            stack.append(f'<li class="cabrow" aria-label="{esc(label)}"><span class="cabrow-in">{esc(label)}</span></li>')
            pending_cab.clear()
    for dk in DECKS:
        if dk.get("cab"):  # 객실 전용 층(20·15·13·12)은 버튼 대신 구간 표시 한 줄로
            pending_cab.append(dk["n"]); continue
        flush_cab()
        cats = []
        for v in dk["v"]:
            if v[2] not in cats: cats.append(v[2])
        if dk.get("cab"):
            lbl = f'<span class="lbl">{esc(deck_title(dk,L))}</span>'
        else:
            ticks = "".join(f'<i style="background:var(--c-{c})" title="{esc(tr(CATS[c],L))}"></i>' for c in cats)
            lbl = f'<span class="lbl"><span class="ticks">{ticks}</span></span>'
        aria = f'{esc(u["deck_aria"].format(n=dk["n"]))}{esc(deck_title(dk,L))}'
        if dk.get("cab"):  # 객실 전용 층은 이동할 섹션이 없으므로 링크가 아닌 표시용
            stack.append(f'<li><span class="deckbtn cabins" data-deck="{dk["n"]}" aria-label="{aria}"><span class="n">{dk["n"]}</span>{lbl}</span></li>')
        else:
            stack.append(f'<li><a class="deckbtn" href="#d{dk["n"]}" data-deck="{dk["n"]}" aria-label="{aria}"><span class="n">{dk["n"]}</span>{lbl}</a></li>')
    flush_cab()

    # 층 섹션
    secs = []
    for dk in DECKS:
        if dk.get("cab"): continue
        items = []
        for name, desc, c, lock in dk["v"]:
            d = tr(desc, L)
            paid = PAID.get(name) if not lock else None
            hrs = hours_for(name, L) if not lock else ""
            text = " ".join(filter(None, [name, d, hrs, tr(CATS[c],L), CATS[c]["ko"], CATS[c]["en"],
                   (u["lbl_paid"] if paid=="paid" else u["lbl_partpaid"] if paid=="part" else ""),
                   ("buffet " + u["lbl_buffet"]) if name in BUFFET else "",
                   ("main dining " + u["lbl_main"]) if name in MAIN else "",
                   ("movie cinema 영화 映画 电影") if name in MOVIE else "", SYN[c]])).lower()
            labels = [f'<span class="cat" style="color:var(--c-{c});background:color-mix(in srgb,var(--c-{c}) 12%,transparent)">{esc(tr(CATS[c],L))}</span>']
            if name in MOVIE: labels.append(f'<span class="movie">🎬 {esc(u["lbl_cinema"] if MOVIE[name]=="cinema" else u["lbl_screen"])}</span>')
            if name in MAIN: labels.append(f'<span class="main">🍽️ {esc(u["lbl_main"])}</span>')
            if name in BUFFET: labels.append(f'<span class="buffet">🍱 {esc(u["lbl_buffet"])}</span>')
            if paid: labels.append(f'<span class="paid">💰 {esc(u["lbl_paid"] if paid=="paid" else u["lbl_partpaid"])}</span>')
            if lock: labels.append(f'<span class="lock">🔒 {esc(u["lbl_lock"])}</span>')
            nm = f'<s>{esc(name)}</s><span class="sr"> {esc(u["concierge_only"])}</span>' if lock else esc(name)
            items.append(
              f'<li class="v{" concierge" if lock else ""}" data-cat="{c}" data-paid="{1 if paid else ""}" data-buffet="{1 if name in BUFFET else ""}" '
              f'data-main="{1 if name in MAIN else ""}" data-movie="{1 if name in MOVIE else ""}" data-text="{esc(text)}">'
              f'<span class="tag" style="background:color-mix(in srgb,var(--c-{c}) 16%,transparent)" title="{esc(tr(CATS[c],L))}" aria-label="{esc(tr(CATS[c],L))}">{CATS[c]["e"]}</span>'
              f'<span><span class="name">{nm}</span><span class="labels">{"".join(labels)}</span>'
              + (f'<span class="ko">{esc(d)}</span>' if d else "") + (f'<span class="hrs">🕒 {esc(hrs)}</span>' if hrs else "") + '</span></li>')
        desc_html = f'<p class="deck-desc">{esc(tr(dk["d"],L))}</p>' if dk.get("d") else ""
        secs.append(
          f'<section class="deck" id="d{dk["n"]}" data-deck="{dk["n"]}" aria-labelledby="h{dk["n"]}">'
          f'<div class="deck-head"><span class="deck-num" aria-hidden="true">{dk["n"]}<small>{esc(u["deck_unit"])}</small></span>'
          f'<div><h2 class="deck-title" id="h{dk["n"]}"><span class="sr">{esc(u["deck_aria"].format(n=dk["n"]))}</span>{esc(deck_title(dk,L))}</h2></div>{desc_html}</div>'
          f'<ul class="venues">{"".join(items)}</ul></section>')

    # 칩
    used = []
    for dk in DECKS:
        for v in dk["v"]:
            if v[2] not in used: used.append(v[2])
    chips = {"all": f'<button class="chip" type="button" data-cat="all" aria-pressed="true">{esc(u["all"])}</button>'}
    for k in used:
        chips[k] = f'<button class="chip" type="button" data-cat="{k}" aria-pressed="false"><span class="dot" style="background:var(--c-{k})"></span>{CATS[k]["e"]} {esc(tr(CATS[k],L))}</button>'
    chips["paid"] = f'<button class="chip" type="button" data-cat="paid" aria-pressed="false"><span class="dot" style="background:var(--paid)"></span>💰 {esc(u["paid_chip"])}</button>'
    chips["movie"] = f'<button class="chip" type="button" data-cat="movie" aria-pressed="false"><span class="dot" style="background:var(--c-show)"></span>🎬 {esc(u["movie_chip"])}</button>'
    chips["main"] = f'<button class="chip" type="button" data-cat="main" aria-pressed="false"><span class="dot" style="background:var(--hull)"></span>🍽️ {esc(u["main_chip"])}</button>'
    chips["buffet"] = f'<button class="chip" type="button" data-cat="buffet" aria-pressed="false"><span class="dot" style="background:var(--c-dining)"></span>🍱 {esc(u["buffet_chip"])}</button>'
    chips_html = "".join(chips[k] for k in CHIP_ORDER if k in chips)

    notes = "".join(f'<p><strong>{esc(a)}</strong>{esc(b)}</p>' for a, b in u["notes"])
    facts = "".join(f'<li>{esc(a)} <b>{esc(b)}</b>{(" "+esc(c)) if c else ""}</li>' for a, b, c in u["facts"])
    lang_links = " ".join(
        f'<a href="{BASE}/{x}/" hreflang="{HREFLANG[x]}" lang="{HREFLANG[x]}" data-lang="{x}"' + (' aria-current="page"' if x == L else "") + f'>{LANG_NAME[x]}</a>'
        for x in LANGS)

    # JSON-LD: 페이지 + 빵부스러기 + 층별 시설 목록
    deck_items = []
    pos = 0
    for dk in DECKS:
        if dk.get("cab"): continue
        pos += 1
        deck_items.append({"@type": "ListItem", "position": pos, "url": f"{url}#d{dk['n']}",
            "item": {"@type": "Place", "name": f"Deck {dk['n']} – {deck_title(dk,L)}",
                     "description": (tr(dk["d"],L) if dk.get("d") else "") or None,
                     "containsPlace": [{"@type": "Place", "name": n, **({"description": " · ".join(filter(None, [tr(d,L), hours_for(n,L) if not l else ""]))} if (tr(d,L) or hours_for(n,L)) else {})} for n, d, c, l in dk["v"]]}})
    for it in deck_items:
        if it["item"]["description"] is None: del it["item"]["description"]
    ld = [
      {"@context": "https://schema.org", "@type": "WebPage", "@id": url, "url": url, "name": u["title"], "description": u["desc"],
       "inLanguage": hl, "dateModified": UPDATED, "isPartOf": {"@type": "WebSite", "name": "수수라이프", "url": SITE + "/"},
       "author": {"@type": "Person", "name": "수수", "url": SITE + "/about/"},
       "about": {"@type": "Thing", "name": "Disney Adventure (Disney Cruise Line)", "sameAs": "https://en.wikipedia.org/wiki/Disney_Adventure"},
       "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITE}/assets/images/disney_adventure_singapore.jpg"},
       "mainEntity": {"@type": "ItemList", "name": u["title"], "numberOfItems": len(deck_items), "itemListOrder": "https://schema.org/ItemListOrderDescending", "itemListElement": deck_items}},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "수수라이프", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": u["title"], "item": url}]},
    ]
    ld_json = json.dumps(ld, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    return f'''<!DOCTYPE html>
<html lang="{hl}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(u["title"])} | 수수라이프</title>
<meta name="description" content="{esc(u["desc"])}">
<link rel="canonical" href="{url}">
{alternates}
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(u["title"])}">
<meta property="og:description" content="{esc(u["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/images/disney_adventure_singapore.jpg">
<meta property="og:locale" content="{OG_LOCALE[L]}">
<meta property="og:site_name" content="수수라이프">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="icon" href="/assets/img/favicons/favicon.ico">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css">
<link rel="stylesheet" href="{BASE}/assets/style.css">
<script type="application/ld+json">{ld_json}</script>
</head>
<body data-lang="{L}" data-result-tpl="{esc(u["result"])}">
<header class="top wrap">
  <nav class="langnav" aria-label="{esc(u["lang_label"])}">
    <a class="back" href="{SITE}/">{esc(u["back"])}</a>
    <span class="langs">{lang_links}</span>
  </nav>
  <div class="titlerow">
    <div>
      <h1>{u["h1"]}</h1>
      <p class="sub">{esc(u["sub"])}</p>
    </div>
    <button class="theme-btn" id="themeBtn" type="button" aria-label="{esc(u["theme_aria"])}">🌓 {esc(u["theme"])}</button>
  </div>
  <ul class="facts">{facts}</ul>
</header>

<div class="controls">
  <div class="wrap">
    <label for="q" class="sr">{esc(u["search_label"])}</label>
    <input id="q" class="search" type="search" placeholder="{esc(u["search_ph"])}" autocomplete="off">
    <div class="chips" id="chips" role="group" aria-label="{esc(u["filter_label"])}">{chips_html}</div>
    <div class="result" id="result" aria-live="polite"></div>
  </div>
</div>

<main class="wrap grid">
  <nav class="ship" aria-label="{esc(u["ship_nav"])}">
    <p class="ship-label">{esc(u["ship_label"])}</p>
    <ul class="stack" id="stack">{"".join(stack)}</ul>
    <div class="hull" aria-hidden="true">{esc(u["hull"])}</div>
    <div class="waterline" aria-hidden="true"></div>
  </nav>
  <div>
    <div id="decks">{"".join(secs)}</div>
    <p class="none-found" id="none">{esc(u["none"])}</p>
    <aside class="notes" aria-label="{esc(u["notes_aria"])}">{notes}</aside>
    <footer class="foot"><p>{esc(u["updated"])}: <time datetime="{UPDATED}">{UPDATED}</time> · <a href="{SITE}/">수수라이프 soosoo.life</a></p></footer>
  </div>
</main>
<script src="{BASE}/assets/app.js" defer></script>
</body>
</html>
'''

def render_root():
    alternates = "\n".join(f'<link rel="alternate" hreflang="{HREFLANG[x]}" href="{SITE}{BASE}/{x}/">' for x in LANGS)
    links = "".join(f'<li><a href="{BASE}/{x}/" hreflang="{HREFLANG[x]}" lang="{HREFLANG[x]}">{LANG_NAME[x]} — {esc(ui_for(x)["title"])}</a></li>' for x in LANGS)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Disney Adventure Deck-by-Deck Guide · 디즈니 어드벤처호 층별 시설 가이드 | 수수라이프</title>
<meta name="description" content="Deck-by-deck public venue guide for Disney Adventure (Singapore). Available in 한국어, English, 日本語, 简体中文, 繁體中文.">
<link rel="canonical" href="{SITE}{BASE}/">
{alternates}
<link rel="alternate" hreflang="x-default" href="{SITE}{BASE}/">
<meta property="og:title" content="Disney Adventure Deck-by-Deck Guide">
<meta property="og:image" content="{SITE}/assets/images/disney_adventure_singapore.jpg">
<link rel="icon" href="/assets/img/favicons/favicon.ico">
<link rel="stylesheet" href="{BASE}/assets/style.css">
<script>
/* 브라우저 언어(또는 이전 선택)에 맞는 언어 페이지로 이동. 검색엔진은 아래 링크 목록을 따라간다. */
(function(){{
  var saved=null; try{{saved=localStorage.getItem('da-lang')}}catch(e){{}}
  var langs=(navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'en']).map(function(l){{return String(l).toLowerCase()}});
  var pick=saved;
  if(!pick){{ for(var i=0;i<langs.length&&!pick;i++){{ var l=langs[i]; if(l.indexOf('ko')===0)pick='ko'; else if(l.indexOf('ja')===0)pick='ja'; else if(l.indexOf('zh')===0)pick=(/zh-(tw|hk|mo|hant)/.test(l)?'zh-tw':'zh-cn'); else if(l.indexOf('en')===0)pick='en'; }} }}
  if(!pick)pick='en';
  location.replace('{BASE}/'+pick+'/');
}})();
</script>
</head>
<body>
<main class="wrap" style="padding-top:40px">
  <h1>Disney Adventure Deck-by-Deck Guide</h1>
  <p class="sub">Choose a language · 언어를 선택하세요 · 言語を選択 · 选择语言 · 選擇語言</p>
  <ul class="langlist">{links}</ul>
</main>
</body>
</html>
'''

CSS = r'''
:root{
  --bg:#F4F7FB; --surface:#FFFFFF; --ink:#142033; --muted:#566377; --line:#DAE2EC;
  --hull:#1B3A6B; --hull-ink:#FFFFFF; --red:#C8372D; --gold:#B57A00; --dim:#A9B4C3;
  --c-dining:#D9480F; --c-cafe:#A0632A; --c-bar:#8E44AD; --c-show:#C2255C; --c-kids:#2B8A3E;
  --c-pool:#1971C2; --c-ride:#E8590C; --c-shop:#5F3DC4; --c-well:#0C8599; --c-svc:#495057; --c-space:#B57A00; --c-etc:#868E96; --paid:#B02A1E;
  box-sizing:border-box; padding-top:env(safe-area-inset-top,0px); padding-bottom:env(safe-area-inset-bottom,0px); color-scheme:light;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#0C1524; --surface:#142135; --ink:#E9EEF5; --muted:#9DABBF; --line:#26354D;
    --hull:#24477F; --red:#FF6B5E; --gold:#F2BC45; --dim:#4A5A72;
    --c-dining:#FF8A4C; --c-cafe:#D9A066; --c-bar:#C38BE0; --c-show:#F06595; --c-kids:#69DB7C;
    --c-pool:#4DABF7; --c-ride:#FFA94D; --c-shop:#9775FA; --c-well:#3BC9DB; --c-svc:#ADB5BD; --c-space:#F2BC45; --c-etc:#ADB5BD; --paid:#FF8A80;
    color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#0C1524; --surface:#142135; --ink:#E9EEF5; --muted:#9DABBF; --line:#26354D;
  --hull:#24477F; --red:#FF6B5E; --gold:#F2BC45; --dim:#4A5A72;
  --c-dining:#FF8A4C; --c-cafe:#D9A066; --c-bar:#C38BE0; --c-show:#F06595; --c-kids:#69DB7C;
  --c-pool:#4DABF7; --c-ride:#FFA94D; --c-shop:#9775FA; --c-well:#3BC9DB; --c-svc:#ADB5BD; --c-space:#F2BC45; --c-etc:#ADB5BD; --paid:#FF8A80;
  color-scheme:dark;
}
html{scroll-padding-top:calc(var(--ctl-h,150px) + var(--strip-h,0px) + 12px);scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Pretendard Variable",Pretendard,-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Hiragino Sans","Malgun Gothic","Noto Sans KR","Noto Sans JP","Noto Sans SC","Noto Sans CJK KR",sans-serif;
  font-size:16px;line-height:1.7;word-break:keep-all;-webkit-text-size-adjust:100%}
.wrap{max-width:1120px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
@media (max-width:820px){.wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
a{color:inherit}
:focus-visible{outline:3px solid var(--gold);outline-offset:2px;border-radius:6px}
.sr{position:absolute;left:-9999px}

/* language nav */
.langnav{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px 16px;padding-top:14px;font-size:.85rem;color:var(--muted)}
.langnav .back{text-decoration:none}
.langnav .langs a{text-decoration:none;padding:4px 9px;border-radius:999px;border:1px solid var(--line);background:var(--surface);margin-left:4px;display:inline-block}
.langnav .langs a[aria-current="page"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.langlist{list-style:none;padding:0;margin:20px 0}
.langlist li{margin:8px 0}
.langlist a{display:block;padding:12px 16px;border:1px solid var(--line);background:var(--surface);border-radius:12px;text-decoration:none}

/* header */
header.top{padding-top:8px;padding-bottom:8px}
.titlerow{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-top:14px}
h1{font-size:clamp(1.6rem,4.5vw,2.4rem);line-height:1.25;margin:0;font-weight:900;letter-spacing:-0.02em}
.sub{color:var(--muted);margin:8px 0 0;max-width:60ch}
.theme-btn{flex:none;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:8px 14px;font:inherit;font-size:.9rem;cursor:pointer;min-height:44px}
.facts{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 0;padding:0;list-style:none}
.facts li{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:6px 12px;font-size:.9rem}
.facts b{color:var(--hull)}
:root[data-theme="dark"] .facts b{color:var(--gold)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .facts b{color:var(--gold)}}

/* controls */
.controls{position:sticky;top:0;z-index:20;background:var(--bg);padding-top:12px;padding-bottom:10px;border-bottom:1px solid var(--line)}
.search{width:100%;font:inherit;padding:10px 14px;border-radius:12px;border:1px solid var(--line);background:var(--surface);color:var(--ink);min-height:44px}
.chips{display:flex;gap:6px;overflow-x:auto;padding:10px 0 2px;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.chip{flex:none;display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:6px 12px;font:inherit;font-size:.88rem;cursor:pointer;min-height:36px}
.chip .dot{width:9px;height:9px;border-radius:50%}
.chip[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.result{font-size:.85rem;color:var(--muted);margin-top:6px}
.result:empty{display:none}

/* layout */
.grid{display:grid;grid-template-columns:200px minmax(0,1fr);min-width:0;gap:28px;padding-top:24px;padding-bottom:40px}

/* ship cross-section */
.ship{position:sticky;top:calc(var(--ctl-h,150px) + 16px);align-self:start;min-width:0;max-height:calc(100vh - var(--ctl-h,150px) - 32px);overflow-y:auto;scrollbar-width:thin}
.grid>div{min-width:0}
.ship-label{font-size:.82rem;color:var(--muted);margin:0 0 8px 4px}
.stack{list-style:none;margin:0;padding:6px;background:var(--surface);border:1px solid var(--line);border-radius:22px 22px 10px 10px;overflow:hidden}
.stack li+li{margin-top:3px}
.deckbtn{display:flex;align-items:center;gap:10px;width:100%;text-decoration:none;padding:3px 8px;border-radius:10px;min-height:30px}
.deckbtn:hover{background:var(--bg)}
.deckbtn .n{font-weight:900;font-variant-numeric:tabular-nums;width:2.1em;text-align:right;font-size:1.05rem;color:var(--hull)}
:root[data-theme="dark"] .deckbtn .n{color:var(--ink)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .deckbtn .n{color:var(--ink)}}
.deckbtn .ticks{display:flex;gap:3px;flex-wrap:wrap}
.deckbtn .ticks i{width:7px;height:7px;border-radius:2px;display:block}
.deckbtn.cabins .n{color:var(--dim)}
.deckbtn.cabins .lbl{font-size:.75rem;color:var(--dim)}
.deckbtn.active{background:var(--hull)}
.deckbtn.active .n,.deckbtn.active .lbl{color:var(--hull-ink)}
.cabrow{margin:3px 0}
.cabrow-in{display:block;font-size:.72rem;color:var(--dim);text-align:center;padding:3px 6px;border:1px dashed var(--line);border-radius:8px;background:var(--bg)}
.hull{background:var(--red);color:#fff;font-size:.75rem;text-align:center;padding:6px;border-radius:6px 6px 14px 14px;margin-top:4px}
.waterline{height:6px;background:repeating-linear-gradient(90deg,var(--c-pool) 0 10px,transparent 10px 16px);opacity:.5;margin-top:6px;border-radius:3px}

/* deck sections */
.deck{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px 22px;margin-bottom:16px}
.deck.hidden{display:none}
.deck-head{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:12px}
.deck-num{font-size:2.6rem;font-weight:900;line-height:1;color:var(--hull);font-variant-numeric:tabular-nums;letter-spacing:-0.03em}
:root[data-theme="dark"] .deck-num{color:var(--gold)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .deck-num{color:var(--gold)}}
.deck-num small{font-size:1rem;font-weight:700;margin-left:2px}
.deck-title{margin:0;font-size:1.15rem;font-weight:700}
.deck-desc{margin:2px 0 0;color:var(--muted);font-size:.93rem;width:100%}
.venues{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(230px,100%),1fr));gap:6px 18px}
.v{min-width:0;display:flex;gap:10px;align-items:flex-start;padding:7px 0;border-bottom:1px dashed var(--line)}
.v.hidden{display:none}
.v>span:last-child{min-width:0}
.v .tag{flex:none;width:26px;height:26px;border-radius:8px;display:grid;place-items:center;font-size:.85rem;margin-top:1px}
.v .name{font-weight:700;line-height:1.35;overflow-wrap:anywhere}
.v .ko{display:block;font-size:.85rem;color:var(--muted);font-weight:400;line-height:1.45}
.v .hrs{display:block;font-size:.8rem;color:var(--muted);line-height:1.45;margin-top:2px}
.v.concierge .name s{text-decoration-thickness:2px;color:var(--muted)}
.v.concierge .ko{text-decoration:line-through}
.labels{display:flex;flex-wrap:wrap;gap:4px;margin:3px 0 1px}
.cat,.movie,.main,.buffet,.paid{display:inline-block;font-size:.74rem;font-weight:700;border-radius:6px;padding:1px 7px;line-height:1.5}
.movie{color:#fff;background:var(--c-show)}
.main{color:var(--hull);border:1px solid currentColor}
:root[data-theme="dark"] .main{color:var(--gold)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .main{color:var(--gold)}}
.buffet{color:#fff;background:var(--c-dining)}
.paid{color:var(--paid);border:1px solid currentColor}
.lock{display:inline-block;font-size:.72rem;font-weight:700;color:var(--gold);border:1px solid currentColor;border-radius:6px;padding:0 5px;line-height:1.5}
.notes{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--red);border-radius:12px;padding:14px 18px;font-size:.92rem;color:var(--muted)}
.notes p{margin:4px 0}
.notes strong{color:var(--ink)}
.none-found{display:none;padding:30px;text-align:center;color:var(--muted)}
.foot{font-size:.82rem;color:var(--muted);margin-top:18px}
.foot a{text-decoration:none}

@media (max-width:820px){
  .grid{grid-template-columns:minmax(0,1fr);gap:12px;padding-top:12px}
  .ship{position:sticky;top:var(--ctl-h,150px);z-index:15;max-height:none;overflow:visible;background:var(--bg);padding:8px 0;margin:-8px 0 0}
  .ship-label{display:none}
  .stack{display:flex;overflow-x:auto;border-radius:12px;gap:4px;scrollbar-width:none}
  .stack::-webkit-scrollbar{display:none}
  .stack li+li{margin-top:0}
  .deckbtn{flex-direction:column;gap:2px;min-width:52px;padding:6px}
  .deckbtn .n{width:auto;text-align:center}
  .deckbtn .lbl{display:none}
  .deckbtn.cabins .lbl{display:none}
  .deckbtn .ticks{justify-content:center;max-width:44px}
  .hull,.waterline{display:none}
  .cabrow{flex:none;display:flex;align-items:center}
  .cabrow-in{font-size:.68rem;padding:4px 8px;white-space:nowrap;border-radius:999px}
  .deck{padding:16px}
  .deck-num{font-size:2.1rem}
}
'''

JS = r'''/* 디즈니 어드벤처 가이드 — 서버 렌더링된 DOM 위에서 필터·테마·활성 층 표시만 담당 */
(function(){
  var $=function(s){return document.querySelector(s)};
  var root=document.documentElement, stack=$("#stack"), chipsEl=$("#chips"), q=$("#q");
  var tpl=document.body.dataset.resultTpl||"{n}";
  var activeCat=null;

  function sync(){
    var text=q.value.trim().toLowerCase();
    chipsEl.querySelectorAll(".chip").forEach(function(b){b.setAttribute("aria-pressed",String((b.dataset.cat==="all"?null:b.dataset.cat)===activeCat))});
    var total=0, filtering=!!(text||activeCat);
    document.querySelectorAll(".deck").forEach(function(sec){
      var n=0;
      sec.querySelectorAll(".v").forEach(function(v){
        var ok=(!activeCat||(activeCat==="paid"?!!v.dataset.paid:activeCat==="buffet"?!!v.dataset.buffet:activeCat==="main"?!!v.dataset.main:activeCat==="movie"?!!v.dataset.movie:v.dataset.cat===activeCat))&&(!text||v.dataset.text.indexOf(text)>-1);
        v.classList.toggle("hidden",!ok); if(ok)n++;
      });
      sec.classList.toggle("hidden",n===0); total+=n;
      var btn=stack.querySelector('[data-deck="'+sec.dataset.deck+'"]');
      if(btn) btn.style.opacity=(filtering&&n===0)?".35":"";
    });
    $("#none").style.display=total?"none":"block";
    var vis=[].slice.call(document.querySelectorAll(".deck:not(.hidden)"));
    var top=(parseFloat(getComputedStyle(root).getPropertyValue("--ctl-h"))||150)+80;
    var cur=vis.filter(function(x){return x.getBoundingClientRect().bottom>top})[0]||vis[0];
    stack.querySelectorAll(".deckbtn").forEach(function(a){a.classList.toggle("active",!!cur&&a.dataset.deck===cur.dataset.deck)});
    $("#result").textContent=filtering?tpl.replace("{n}",total):"";
  }
  chipsEl.addEventListener("click",function(e){
    var b=e.target.closest(".chip"); if(!b)return;
    var k=b.dataset.cat; activeCat=(k==="all"||activeCat===k)?null:k; sync();
  });
  q.addEventListener("input",sync);

  /* active deck highlight while scrolling */
  if("IntersectionObserver" in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(!e.isIntersecting)return;
        stack.querySelectorAll(".deckbtn").forEach(function(a){a.classList.toggle("active",a.dataset.deck===e.target.dataset.deck)});
        var a=stack.querySelector('[data-deck="'+e.target.dataset.deck+'"]');
        if(a&&window.innerWidth<=820){stack.scrollTo({left:a.offsetLeft-(stack.clientWidth-a.offsetWidth)/2,behavior:"smooth"})}
      });
    },{rootMargin:"-40% 0px -55% 0px"});
    document.querySelectorAll(".deck").forEach(function(s){io.observe(s)});
  }

  /* theme */
  try{var t=localStorage.getItem("da-theme");if(t)root.dataset.theme=t}catch(e){}
  $("#themeBtn").onclick=function(){
    var cur=root.dataset.theme||(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light");
    var next=cur==="dark"?"light":"dark"; root.dataset.theme=next;
    try{localStorage.setItem("da-theme",next)}catch(e){}
  };

  /* remember language choice (root page redirects to it next time) */
  document.querySelectorAll(".langnav a[data-lang]").forEach(function(a){
    a.addEventListener("click",function(){try{localStorage.setItem("da-lang",a.dataset.lang)}catch(e){}});
  });
  try{localStorage.setItem("da-lang",document.body.dataset.lang)}catch(e){}

  function measure(){
    var c=document.querySelector(".controls").offsetHeight;
    root.style.setProperty("--ctl-h",c+"px");
    var mob=window.innerWidth<=820;
    root.style.setProperty("--strip-h",mob?document.querySelector(".ship").offsetHeight+"px":"0px");
  }
  measure();
  if("ResizeObserver" in window){new ResizeObserver(measure).observe(document.querySelector(".controls"))}
  addEventListener("resize",measure);
  sync();
})();
'''

def main():
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    for L in LANGS:
        os.makedirs(os.path.join(ROOT, L), exist_ok=True)
        with open(os.path.join(ROOT, L, "index.html"), "w", encoding="utf-8") as f: f.write(render_lang(L))
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f: f.write(render_root())
    # 초기 배포 때 쓰던 /zh/ 경로는 /zh-cn/ 으로 안내
    os.makedirs(os.path.join(ROOT, "zh"), exist_ok=True)
    with open(os.path.join(ROOT, "zh", "index.html"), "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html><html lang="zh-Hans"><head><meta charset="utf-8"><title>Redirecting…</title><meta name="robots" content="noindex"><link rel="canonical" href="{SITE}{BASE}/zh-cn/"><meta http-equiv="refresh" content="0; url={BASE}/zh-cn/"><script>location.replace("{BASE}/zh-cn/")</script></head><body><a href="{BASE}/zh-cn/">简体中文</a></body></html>\n')
    with open(os.path.join(ROOT, "assets", "style.css"), "w", encoding="utf-8") as f: f.write(CSS.strip() + "\n")
    with open(os.path.join(ROOT, "assets", "app.js"), "w", encoding="utf-8") as f: f.write(JS)
    print("generated:", ", ".join(f"{L}/index.html" for L in LANGS), "+ index.html, assets/style.css, assets/app.js")

if __name__ == "__main__":
    main()
