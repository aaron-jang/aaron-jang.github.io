/* 디즈니 어드벤처 가이드 — 서버 렌더링된 DOM 위에서 필터·테마·활성 층 표시만 담당 */
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
