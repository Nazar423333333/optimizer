// ============================================================
// WINDOWS OPTIMIZER ULTRA 6.2.1
// SCRIPT.JS
// ============================================================

const translations = {
    uk: {
        home: "Головна",
        features: "Можливості",
        download: "Завантаження",
        faq: "FAQ",

        badge: "● Версія 6.2.1",

        hero1: "Оптимізуй Windows",
        hero2: "в одному застосунку",

        heroText:
            "Очищення, моніторинг, системна діагностика, Ultimate Performance, DISM, SFC, інструменти Windows та багато іншого.",

        downloadBtn: "Завантажити EXE",
        learnMore: "Дізнатися більше",

        version: "Версія",
        languages: "Мов",
        support: "Підтримка",

        systemStatus: "СТАН СИСТЕМИ",
        good: "Все добре",

        featuresEyebrow: "МОЖЛИВОСТІ",
        featuresTitle: "Все необхідне для Windows",

        featuresText:
            "Основні інструменти зібрані в одному сучасному інтерфейсі.",

        cleaningTitle: "Очищення",
        repairTitle: "Repair Center",
        monitorTitle: "Моніторинг",
        toolsTitle: "Інструменти",
        langTitle: "5 мов",

        f1: "Створення та активація плану максимальної продуктивності.",

        f2:
            "TEMP, DNS, кошик, кеш ескізів і стандартні засоби Windows.",

        f3:
            "SFC, DISM CheckHealth, ScanHealth, RestoreHealth і CHKDSK Scan.",

        f4:
            "CPU, RAM, диски та системна інформація в реальному часі.",

        f5:
            "Device Manager, Event Viewer, Resource Monitor, Services та інше.",

        f6:
            "Українська, English, Polski, Deutsch та Español.",

        downloadEyebrow: "ЗАВАНТАЖЕННЯ",

        downloadText:
            "Завантаж готову версію для Windows.",

        notice:
            "Деякі системні функції можуть запитувати права адміністратора Windows.",

        faqTitle: "Часті запитання",

        q1: "Для якої Windows програма?",
        a1: "Сайт підготовлений для Windows 11 64-bit.",

        q2: "Чому Windows запитує права адміністратора?",

        a2:
            "Вони потрібні лише для системних операцій, які Windows не дозволяє звичайному користувачу.",

        q3: "Як додати EXE на сайт?",

        a3:
            "Поклади Windows_Optimizer_Ultra_6_2_1.exe поруч із index.html."
    },

    // ========================================================
    // ENGLISH
    // ========================================================

    en: {
        home: "Home",
        features: "Features",
        download: "Download",
        faq: "FAQ",

        badge: "● Version 6.2.1",

        hero1: "Optimize Windows",
        hero2: "in one application",

        heroText:
            "Cleaning, monitoring, system diagnostics, Ultimate Performance, DISM, SFC, Windows tools and more.",

        downloadBtn: "Download EXE",
        learnMore: "Learn more",

        version: "Version",
        languages: "Languages",
        support: "Support",

        systemStatus: "SYSTEM STATUS",
        good: "Everything looks good",

        featuresEyebrow: "FEATURES",

        featuresTitle:
            "Everything you need for Windows",

        featuresText:
            "Essential tools collected in one modern interface.",

        cleaningTitle: "Cleaning",
        repairTitle: "Repair Center",
        monitorTitle: "Monitoring",
        toolsTitle: "Tools",
        langTitle: "5 languages",

        f1:
            "Create and activate the Ultimate Performance power plan.",

        f2:
            "TEMP, DNS, Recycle Bin, thumbnail cache and Windows cleanup tools.",

        f3:
            "SFC, DISM CheckHealth, ScanHealth, RestoreHealth and CHKDSK Scan.",

        f4:
            "Real-time CPU, RAM, disk and system information.",

        f5:
            "Device Manager, Event Viewer, Resource Monitor, Services and more.",

        f6:
            "Ukrainian, English, Polish, German and Spanish.",

        downloadEyebrow: "DOWNLOAD",

        downloadText:
            "Download the ready Windows version.",

        notice:
            "Some system functions may request Windows administrator permission.",

        faqTitle:
            "Frequently asked questions",

        q1:
            "Which Windows version is supported?",

        a1:
            "This site is prepared for Windows 11 64-bit.",

        q2:
            "Why does Windows ask for administrator permission?",

        a2:
            "It is only required for system operations that Windows restricts to administrators.",

        q3:
            "How do I add the EXE to the site?",

        a3:
            "Place Windows_Optimizer_Ultra_6_2_1.exe next to index.html."
    },

    // ========================================================
    // POLSKI
    // ========================================================

    pl: {
        home: "Główna",
        features: "Funkcje",
        download: "Pobierz",
        faq: "FAQ",

        badge: "● Wersja 6.2.1",

        hero1: "Optymalizuj Windows",
        hero2: "w jednej aplikacji",

        heroText:
            "Czyszczenie, monitoring, diagnostyka, Ultimate Performance, DISM, SFC i narzędzia Windows.",

        downloadBtn: "Pobierz EXE",
        learnMore: "Dowiedz się więcej",

        version: "Wersja",
        languages: "Języków",
        support: "Wsparcie",

        systemStatus: "STAN SYSTEMU",
        good: "Wszystko działa dobrze",

        featuresEyebrow: "FUNKCJE",

        featuresTitle:
            "Wszystko dla Windows",

        featuresText:
            "Najważniejsze narzędzia w jednym nowoczesnym interfejsie.",

        cleaningTitle: "Czyszczenie",
        repairTitle: "Centrum napraw",
        monitorTitle: "Monitoring",
        toolsTitle: "Narzędzia",
        langTitle: "5 języków",

        f1:
            "Tworzenie i aktywacja planu Ultimate Performance.",

        f2:
            "TEMP, DNS, kosz, pamięć miniaturek i narzędzia Windows.",

        f3:
            "SFC, DISM CheckHealth, ScanHealth, RestoreHealth i CHKDSK Scan.",

        f4:
            "CPU, RAM, dyski i informacje systemowe w czasie rzeczywistym.",

        f5:
            "Menedżer urządzeń, Podgląd zdarzeń, Monitor zasobów, Usługi i więcej.",

        f6:
            "Ukraiński, angielski, polski, niemiecki i hiszpański.",

        downloadEyebrow: "POBIERANIE",

        downloadText:
            "Pobierz gotową wersję dla Windows.",

        notice:
            "Niektóre funkcje mogą wymagać uprawnień administratora.",

        faqTitle: "Najczęstsze pytania",

        q1: "Dla jakiego Windows?",

        a1:
            "Strona jest przygotowana dla Windows 11 64-bit.",

        q2:
            "Dlaczego Windows pyta o administratora?",

        a2:
            "Uprawnienia są wymagane tylko dla operacji systemowych.",

        q3:
            "Jak dodać EXE do strony?",

        a3:
            "Umieść Windows_Optimizer_Ultra_6_2_1.exe obok index.html."
    },

    // ========================================================
    // DEUTSCH
    // ========================================================

    de: {
        home: "Start",
        features: "Funktionen",
        download: "Download",
        faq: "FAQ",

        badge: "● Version 6.2.1",

        hero1: "Windows optimieren",
        hero2: "in einer Anwendung",

        heroText:
            "Bereinigung, Überwachung, Diagnose, Ultimate Performance, DISM, SFC und Windows-Werkzeuge.",

        downloadBtn: "EXE herunterladen",
        learnMore: "Mehr erfahren",

        version: "Version",
        languages: "Sprachen",
        support: "Unterstützung",

        systemStatus: "SYSTEMSTATUS",
        good: "Alles in Ordnung",

        featuresEyebrow: "FUNKTIONEN",

        featuresTitle:
            "Alles für Windows",

        featuresText:
            "Wichtige Werkzeuge in einer modernen Oberfläche.",

        cleaningTitle: "Bereinigung",
        repairTitle: "Reparaturzentrum",
        monitorTitle: "Überwachung",
        toolsTitle: "Werkzeuge",
        langTitle: "5 Sprachen",

        f1:
            "Ultimate-Performance-Energiesparplan erstellen und aktivieren.",

        f2:
            "TEMP, DNS, Papierkorb, Miniaturcache und Windows-Bereinigung.",

        f3:
            "SFC, DISM CheckHealth, ScanHealth, RestoreHealth und CHKDSK Scan.",

        f4:
            "CPU-, RAM-, Datenträger- und Systeminformationen in Echtzeit.",

        f5:
            "Geräte-Manager, Ereignisanzeige, Ressourcenmonitor, Dienste und mehr.",

        f6:
            "Ukrainisch, Englisch, Polnisch, Deutsch und Spanisch.",

        downloadEyebrow: "DOWNLOAD",

        downloadText:
            "Fertige Windows-Version herunterladen.",

        notice:
            "Einige Systemfunktionen können Administratorrechte anfordern.",

        faqTitle:
            "Häufige Fragen",

        q1:
            "Welche Windows-Version?",

        a1:
            "Die Seite ist für Windows 11 64-Bit vorbereitet.",

        q2:
            "Warum werden Administratorrechte benötigt?",

        a2:
            "Nur Systemvorgänge benötigen diese Rechte.",

        q3:
            "Wie füge ich die EXE hinzu?",

        a3:
            "Lege Windows_Optimizer_Ultra_6_2_1.exe neben index.html."
    },

    // ========================================================
    // ESPAÑOL
    // ========================================================

    es: {
        home: "Inicio",
        features: "Funciones",
        download: "Descargar",
        faq: "FAQ",

        badge: "● Versión 6.2.1",

        hero1: "Optimiza Windows",
        hero2: "en una sola aplicación",

        heroText:
            "Limpieza, monitorización, diagnóstico, Ultimate Performance, DISM, SFC y herramientas de Windows.",

        downloadBtn: "Descargar EXE",
        learnMore: "Más información",

        version: "Versión",
        languages: "Idiomas",
        support: "Soporte",

        systemStatus: "ESTADO DEL SISTEMA",
        good: "Todo está bien",

        featuresEyebrow: "FUNCIONES",

        featuresTitle:
            "Todo lo necesario para Windows",

        featuresText:
            "Herramientas esenciales en una interfaz moderna.",

        cleaningTitle: "Limpieza",
        repairTitle: "Centro de reparación",
        monitorTitle: "Monitorización",
        toolsTitle: "Herramientas",
        langTitle: "5 idiomas",

        f1:
            "Crear y activar el plan Ultimate Performance.",

        f2:
            "TEMP, DNS, papelera, caché de miniaturas y herramientas de limpieza.",

        f3:
            "SFC, DISM CheckHealth, ScanHealth, RestoreHealth y CHKDSK Scan.",

        f4:
            "CPU, RAM, discos e información del sistema en tiempo real.",

        f5:
            "Administrador de dispositivos, Visor de eventos, Monitor de recursos, Servicios y más.",

        f6:
            "Ucraniano, inglés, polaco, alemán y español.",

        downloadEyebrow: "DESCARGA",

        downloadText:
            "Descarga la versión preparada para Windows.",

        notice:
            "Algunas funciones pueden solicitar permisos de administrador.",

        faqTitle:
            "Preguntas frecuentes",

        q1:
            "¿Para qué versión de Windows?",

        a1:
            "La página está preparada para Windows 11 de 64 bits.",

        q2:
            "¿Por qué pide permisos de administrador?",

        a2:
            "Solo se requieren para operaciones del sistema.",

        q3:
            "¿Cómo añado el EXE al sitio?",

        a3:
            "Coloca Windows_Optimizer_Ultra_6_2_1.exe junto a index.html."
    }
};


// ============================================================
// LANGUAGE SYSTEM
// ============================================================

function setLanguage(lang) {

    if (!translations[lang]) {
        lang = "uk";
    }

    document.documentElement.lang = lang;

    const elements =
        document.querySelectorAll("[data-i18n]");

    elements.forEach((element) => {

        const key =
            element.getAttribute("data-i18n");

        const translatedText =
            translations[lang][key];

        if (translatedText) {
            element.textContent = translatedText;
        }

    });

    // Запам'ятовуємо вибір
    localStorage.setItem(
        "optimizerLanguage",
        lang
    );
}


// ============================================================
// LANGUAGE SELECT
// ============================================================

const languageSelect =
    document.getElementById("language");

if (languageSelect) {

    const savedLanguage =
        localStorage.getItem(
            "optimizerLanguage"
        ) || "uk";

    languageSelect.value =
        savedLanguage;

    setLanguage(savedLanguage);

    languageSelect.addEventListener(
        "change",
        function () {

            setLanguage(
                languageSelect.value
            );

        }
    );
}


// ============================================================
// SMOOTH SCROLL
// ============================================================

document
    .querySelectorAll('a[href^="#"]')
    .forEach((link) => {

        link.addEventListener(
            "click",
            function (event) {

                const href =
                    this.getAttribute("href");

                if (!href || href === "#") {
                    return;
                }

                const target =
                    document.querySelector(href);

                if (!target) {
                    return;
                }

                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }
        );

    });


// ============================================================
// DOWNLOAD BUTTON
// ============================================================

const downloadButtons =
    document.querySelectorAll(
        'a[href$=".exe"]'
    );

downloadButtons.forEach((button) => {

    button.addEventListener(
        "click",
        function () {

            console.log(
                "Downloading Windows Optimizer Ultra 6.2.1..."
            );

        }
    );

});


// ============================================================
// NAVBAR SCROLL EFFECT
// ============================================================

const header =
    document.querySelector(".topbar");

window.addEventListener(
    "scroll",
    function () {

        if (!header) {
            return;
        }

        if (window.scrollY > 30) {

            header.classList.add(
                "scrolled"
            );

        } else {

            header.classList.remove(
                "scrolled"
            );

        }

    }
);


// ============================================================
// FAQ
// ============================================================

const faqItems =
    document.querySelectorAll(
        ".faq-list details"
    );

faqItems.forEach((item) => {

    item.addEventListener(
        "toggle",
        function () {

            if (!item.open) {
                return;
            }

            // Закриваємо інші FAQ
            faqItems.forEach(
                (otherItem) => {

                    if (
                        otherItem !== item
                    ) {
                        otherItem.open = false;
                    }

                }
            );

        }
    );

});


// ============================================================
// INITIALIZED
// ============================================================

console.log(
    "%c Windows Optimizer Ultra 6.2.1 ",
    "background:#1774ff;color:white;font-size:16px;padding:8px;border-radius:6px;"
);

console.log(
    "Website initialized successfully."
);