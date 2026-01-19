// 다크모드 토글 기능
(function() {
  'use strict';

  // 현재 테마 가져오기 (localStorage 또는 시스템 설정)
  function getCurrentTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      return savedTheme;
    }
    // 시스템 다크모드 설정 확인
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  }

  // 테마 적용
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateToggleButton(theme);
  }

  // 토글 버튼 아이콘 업데이트
  function updateToggleButton(theme) {
    const toggleButton = document.querySelector('.darkmode-toggle');
    if (toggleButton) {
      toggleButton.textContent = theme === 'dark' ? '☀️' : '🌙';
      toggleButton.setAttribute('aria-label', theme === 'dark' ? '라이트 모드로 전환' : '다크 모드로 전환');
    }
  }

  // 테마 토글
  function toggleTheme() {
    const currentTheme = getCurrentTheme();
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);

    // 모바일 메뉴가 열려있으면 닫기
    const navbarCollapse = document.querySelector('#main-navbar');
    if (navbarCollapse && navbarCollapse.classList.contains('show')) {
      const navbarToggler = document.querySelector('.navbar-toggler');
      if (navbarToggler) {
        navbarToggler.click();
      }
    }
  }

  // 페이지 로드 시 테마 적용
  document.addEventListener('DOMContentLoaded', function() {
    const currentTheme = getCurrentTheme();
    applyTheme(currentTheme);

    // 토글 버튼에 이벤트 리스너 추가
    const toggleButton = document.querySelector('.darkmode-toggle');
    if (toggleButton) {
      toggleButton.addEventListener('click', toggleTheme);
    }

    // 초기 로드 완료 - transition 활성화
    requestAnimationFrame(function() {
      document.documentElement.classList.add('loaded');
    });
  });

  // 시스템 테마 변경 감지
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
      // 사용자가 수동으로 설정하지 않은 경우에만 시스템 설정 따름
      if (!localStorage.getItem('theme')) {
        applyTheme(e.matches ? 'dark' : 'light');
      }
    });
  }

  // 즉시 테마 적용 (깜빡임 방지)
  const currentTheme = getCurrentTheme();
  document.documentElement.setAttribute('data-theme', currentTheme);
})();
