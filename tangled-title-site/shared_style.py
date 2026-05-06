import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bwdc-teal: #294943;
            --bwdc-teal-deep: #18312d;
            --bwdc-cream: #fff7dc;
            --bwdc-cream-soft: #fffaf0;
            --bwdc-gold: #efc267;
            --bwdc-gold-deep: #c88f2e;
            --bwdc-sage: #a9c77b;
            --bwdc-mint: #d7e8bd;
            --bwdc-rose: #c96b68;
            --bwdc-blue: #6fa8c8;
            --bwdc-line: #d7ddcf;
            --bwdc-muted: #5d6a64;
        }

        .stApp {
            background:
                linear-gradient(180deg, rgba(255, 247, 220, 0.72), rgba(255, 250, 240, 0.94)),
                #fffaf0;
            color: var(--bwdc-teal-deep);
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }

        h1, h2, h3 {
            color: var(--bwdc-teal-deep);
            letter-spacing: 0 !important;
        }

        p, li {
            color: var(--bwdc-teal-deep);
        }

        section[data-testid="stSidebar"] {
            background: var(--bwdc-teal);
        }

        section[data-testid="stSidebar"] * {
            color: #fffaf0 !important;
        }

        div[data-testid="stSidebarNav"] a {
            border-radius: 8px;
        }

        div[data-testid="stSidebarNav"] a:hover {
            background: rgba(239, 194, 103, 0.18);
        }

        .support-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.65rem;
            padding: 0.55rem 0.8rem;
            border-radius: 8px;
            background: var(--bwdc-teal);
            color: #fffaf0;
            font-weight: 700;
            border: 1px solid rgba(255, 250, 240, 0.3);
        }

        .support-mark {
            width: 28px;
            height: 28px;
            border-radius: 6px;
            background: var(--bwdc-cream);
            position: relative;
            flex: 0 0 auto;
        }

        .support-mark::before {
            content: "";
            position: absolute;
            left: 7px;
            top: 8px;
            width: 14px;
            height: 13px;
            background: var(--bwdc-teal);
            clip-path: polygon(50% 0, 100% 35%, 76% 100%, 24% 100%, 0 35%);
        }

        .section-note {
            color: var(--bwdc-muted);
            font-size: 1.05rem;
            line-height: 1.55;
            max-width: 900px;
        }

        .soft-card {
            border: 1px solid var(--bwdc-line);
            border-radius: 8px;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.82);
            min-height: 142px;
            box-shadow: 0 10px 30px rgba(24, 49, 45, 0.05);
        }

        .soft-card h3 {
            margin-top: 0;
            font-size: 1.05rem;
        }

        .soft-card p {
            color: var(--bwdc-muted);
            line-height: 1.45;
        }

        .takeaway {
            border-left: 5px solid var(--bwdc-sage);
            background: #f1f7df;
            padding: 1rem 1.1rem;
            border-radius: 6px;
            color: var(--bwdc-teal-deep);
        }

        .pathway-scene {
            border: 1px solid var(--bwdc-line);
            border-radius: 8px;
            background: linear-gradient(135deg, #fff7dc 0%, #f4e0a7 100%);
            padding: 1rem;
            overflow: hidden;
        }

        .scene-row {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
            gap: 0.8rem;
            align-items: stretch;
        }

        .scene-step {
            position: relative;
            border: 1px solid rgba(41, 73, 67, 0.2);
            border-radius: 8px;
            padding: 0.85rem;
            background: rgba(255, 250, 240, 0.92);
            min-height: 168px;
        }

        .scene-step::after {
            content: "";
            position: absolute;
            right: -0.58rem;
            top: 50%;
            width: 0.8rem;
            height: 0.8rem;
            border-top: 3px solid var(--bwdc-gold-deep);
            border-right: 3px solid var(--bwdc-gold-deep);
            transform: translateY(-50%) rotate(45deg);
            animation: pulse-arrow 1.6s ease-in-out infinite;
        }

        .scene-step:last-child::after {
            display: none;
        }

        .mini-house {
            width: 58px;
            height: 46px;
            background: var(--bwdc-teal);
            margin-bottom: 0.7rem;
            clip-path: polygon(50% 0, 100% 36%, 100% 100%, 0 100%, 0 36%);
            opacity: 0.95;
        }

        .mini-doc {
            width: 46px;
            height: 54px;
            border-radius: 4px;
            background: #ffffff;
            border: 2px solid var(--bwdc-teal);
            margin-bottom: 0.7rem;
            position: relative;
        }

        .mini-doc::before,
        .mini-doc::after {
            content: "";
            position: absolute;
            left: 9px;
            right: 9px;
            height: 3px;
            background: var(--bwdc-gold-deep);
        }

        .mini-doc::before {
            top: 17px;
        }

        .mini-doc::after {
            top: 29px;
        }

        .mini-lock {
            width: 48px;
            height: 42px;
            border-radius: 7px;
            background: var(--bwdc-rose);
            margin: 0.75rem 0 0.7rem;
            position: relative;
        }

        .mini-lock::before {
            content: "";
            position: absolute;
            left: 10px;
            top: -21px;
            width: 24px;
            height: 25px;
            border: 5px solid var(--bwdc-rose);
            border-bottom: 0;
            border-radius: 16px 16px 0 0;
        }

        .mini-wealth {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: conic-gradient(var(--bwdc-sage), var(--bwdc-gold), var(--bwdc-teal), var(--bwdc-sage));
            margin-bottom: 0.7rem;
        }

        .scene-step strong {
            display: block;
            color: var(--bwdc-teal-deep);
            margin-bottom: 0.35rem;
        }

        .scene-step span {
            color: var(--bwdc-muted);
            font-size: 0.9rem;
            line-height: 1.35;
        }

        @keyframes pulse-arrow {
            0%, 100% { opacity: 0.35; transform: translateY(-50%) translateX(-2px) rotate(45deg); }
            50% { opacity: 1; transform: translateY(-50%) translateX(2px) rotate(45deg); }
        }

        .quote-card {
            border-left: 5px solid var(--bwdc-gold-deep);
            background: #fff7dc;
            border-radius: 8px;
            padding: 1rem 1.1rem;
            font-size: 1.05rem;
            line-height: 1.5;
        }

        .quote-card em {
            color: var(--bwdc-teal-deep);
        }

        .placeholder-map {
            border: 1px dashed rgba(41, 73, 67, 0.38);
            border-radius: 8px;
            background:
                radial-gradient(circle at 28% 22%, rgba(239, 194, 103, 0.6) 0 8%, transparent 9%),
                radial-gradient(circle at 62% 46%, rgba(169, 199, 123, 0.65) 0 10%, transparent 11%),
                radial-gradient(circle at 42% 74%, rgba(201, 107, 104, 0.5) 0 7%, transparent 8%),
                linear-gradient(135deg, #fff7dc, #d7e8bd);
            min-height: 280px;
            padding: 1rem;
            display: flex;
            align-items: end;
            color: var(--bwdc-teal-deep);
            font-weight: 700;
        }

        @media (max-width: 900px) {
            .scene-row {
                grid-template-columns: 1fr;
            }

            .scene-step::after {
                right: 50%;
                top: auto;
                bottom: -0.55rem;
                transform: translateX(50%) rotate(135deg);
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def support_badge() -> None:
    st.markdown(
        """
        <div class="support-badge">
            <span class="support-mark"></span>
            <span>Supported by Black Wealth Data Center</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
