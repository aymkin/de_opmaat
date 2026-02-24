// ==UserScript==
// @name        AnkiWeb Dark + Large Font
// @namespace   ankiweb-dark-custom
// @version     3.0
// @description Dark theme with large fonts for AnkiWeb mobile (all pages)
// @author      Claude
// @match       https://ankiweb.net/*
// @match       https://ankiuser.net/*
// @grant       none
// @run-at      document-start
// ==/UserScript==

(function() {
    'use strict';

    const css = `
    /* ==============================
       GLOBAL
       ============================== */
    *, *::before, *::after {
        border-color: #2a2a4a !important;
    }
    body, html {
        background-color: #121220 !important;
        color: #e0e0e0 !important;
        font-size: 18px !important;
        line-height: 1.4 !important;
    }
    /* Убиваем ВСЕ белые фоны */
    div, section, main, article, aside, header, footer,
    .container, .container-fluid, .container-sm,
    .container-md, .container-lg, .container-xl,
    .row, [class*="col-"], .card-body,
    .bg-light, .bg-white {
        background-color: transparent !important;
        color: #e0e0e0 !important;
    }

    /* ==============================
       НАВИГАЦИЯ
       ============================== */
    .navbar, .navbar-light, .navbar-expand-lg, nav {
        background-color: #0d0d1a !important;
        border-bottom: 2px solid #1a3a5c !important;
    }
    .navbar-brand {
        filter: brightness(1.8) !important;
    }
    .navbar-toggler {
        border-color: #666 !important;
    }
    .navbar-toggler-icon {
        filter: invert(1) !important;
    }
    .nav-link, .navbar-nav .nav-link {
        color: #90caf9 !important;
        font-size: 18px !important;
    }
    .navbar-collapse {
        background-color: #0d0d1a !important;
    }

    /* ==============================
       ССЫЛКИ
       ============================== */
    a { color: #64b5f6 !important; }
    a:hover { color: #bbdefb !important; }

    /* ==============================
       СПИСОК КОЛОД — таблица
       ============================== */
    table, .table {
        color: #e0e0e0 !important;
        width: 100% !important;
        table-layout: fixed !important;
    }
    tr, td, th {
        background-color: #121220 !important;
        color: #e0e0e0 !important;
        padding: 10px 8px !important;
        font-size: 18px !important;
        vertical-align: middle !important;
        word-wrap: break-word !important;
    }
    tr:hover td {
        background-color: #1a1a36 !important;
    }
    /* Названия колод */
    td:first-child, td:first-child a {
        font-size: 20px !important;
        font-weight: 500 !important;
    }
    /* Счётчики */
    td:nth-child(2) {
        font-size: 18px !important;
        font-weight: bold !important;
        white-space: nowrap !important;
        width: 50px !important;
    }
    /* Actions колонка — компактнее */
    td:last-child {
        width: 90px !important;
        font-size: 16px !important;
        white-space: nowrap !important;
    }

    /* ==============================
       КНОПКИ
       ============================== */
    .btn, button, input[type="submit"], input[type="button"] {
        background-color: #1a3a5c !important;
        color: #e0e0e0 !important;
        border-color: #2a5a8c !important;
        font-size: 18px !important;
        padding: 10px 16px !important;
        border-radius: 8px !important;
    }
    .btn:hover, button:hover {
        background-color: #2a5a8c !important;
    }
    .btn-primary {
        background-color: #1565c0 !important;
        border-color: #1976d2 !important;
    }
    .btn-link {
        background-color: transparent !important;
        color: #64b5f6 !important;
        border: none !important;
    }
    .btn-outline-secondary {
        color: #bbb !important;
        border-color: #555 !important;
        background-color: transparent !important;
    }

    /* ==============================
       СТРАНИЦА УЧЁБЫ — КАРТОЧКА
       ============================== */
    #qa, #qa_box, .card,
    #studyBox, .study-area,
    #answer, #question {
        background-color: #1a1a30 !important;
        color: #e0e0e0 !important;
        font-size: 24px !important;
        line-height: 1.5 !important;
        padding: 20px !important;
        border-radius: 10px !important;
    }
    #qa *, #qa_box *, .card * {
        color: #e0e0e0 !important;
        line-height: 1.5 !important;
    }
    /* Текст карточки крупный */
    #qa, #qa_box {
        font-size: 26px !important;
    }

    /* Аудио-плеер — тёмный */
    audio {
        filter: invert(1) hue-rotate(180deg) !important;
        width: 90% !important;
        max-width: 350px !important;
        margin: 10px auto !important;
        display: block !important;
    }

    /* Кнопки ответов */
    #ansbuta, #ansbutb, #ansbutc, #ansbutd,
    .btn-answer, .answer-btn {
        font-size: 20px !important;
        padding: 14px 20px !important;
        min-height: 50px !important;
        margin: 4px !important;
    }
    #ansbut, #ansbut button, #ansbut .btn {
        font-size: 20px !important;
        padding: 14px 24px !important;
        min-height: 50px !important;
    }

    /* Область под карточкой — тоже тёмная */
    #studycnt, #studynow, .study-controls,
    #ansbut, #ease-buttons {
        background-color: #121220 !important;
    }

    /* Вся область study */
    body[class*="study"], body {
        background-color: #121220 !important;
    }

    /* iframe внутри карточки (если есть) */
    iframe {
        background-color: #1a1a30 !important;
        border: none !important;
    }

    /* Разделитель ответа */
    hr, #qa hr, hr#answer {
        border-color: #444 !important;
        background-color: #444 !important;
    }

    /* Счётчики карточек сверху (6 + 0 + 26) */
    .study-count, #counts {
        font-size: 20px !important;
    }

    /* ==============================
       DROPDOWN
       ============================== */
    .dropdown-menu {
        background-color: #16213e !important;
        font-size: 18px !important;
    }
    .dropdown-item {
        color: #e0e0e0 !important;
        padding: 10px 16px !important;
    }
    .dropdown-item:hover {
        background-color: #1a1a36 !important;
    }

    /* ==============================
       ФОРМЫ
       ============================== */
    input, textarea, select, .form-control {
        background-color: #1a1a30 !important;
        color: #e0e0e0 !important;
        border-color: #2a2a4a !important;
        font-size: 18px !important;
        padding: 10px !important;
    }
    label { color: #ccc !important; }

    /* ==============================
       МОДАЛЬНЫЕ ОКНА
       ============================== */
    .modal-content {
        background-color: #1a1a30 !important;
        color: #e0e0e0 !important;
    }
    .modal-header, .modal-footer {
        border-color: #2a2a4a !important;
    }

    /* ==============================
       ФУТЕР
       ============================== */
    footer, .footer {
        background-color: #0d0d1a !important;
        color: #666 !important;
    }

    /* ==============================
       РАЗНОЕ
       ============================== */
    .text-muted { color: #999 !important; }
    .text-dark { color: #e0e0e0 !important; }
    .alert {
        background-color: #1a3a5c !important;
        color: #e0e0e0 !important;
    }
    .progress {
        background-color: #2a2a4a !important;
    }
    .progress-bar {
        background-color: #1976d2 !important;
    }
    ::-webkit-scrollbar {
        width: 8px;
        background: #121220;
    }
    ::-webkit-scrollbar-thumb {
        background: #2a2a4a;
        border-radius: 4px;
    }
    `;

    const style = document.createElement('style');
    style.id = 'ankiweb-dark-theme';
    style.textContent = css;

    function inject() {
        // Удаляем старый если есть
        const old = document.getElementById('ankiweb-dark-theme');
        if (old) return;

        const target = document.head || document.documentElement;
        if (target) target.appendChild(style);
    }

    inject();
    document.addEventListener('DOMContentLoaded', inject);
})();