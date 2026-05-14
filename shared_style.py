from html import escape
import json

import streamlit as st
import streamlit.components.v1 as components


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
            padding-bottom: 4rem;
            max-width: 1180px;
        }

        .main .block-container > div {
            max-width: 1180px;
        }

        section[data-testid="stMain"] h2 {
            margin-top: 3.2rem;
            padding-top: 0.15rem;
            border-top: 1px solid rgba(41, 73, 67, 0.12);
        }

        h1, h2, h3 {
            color: var(--bwdc-teal-deep);
            letter-spacing: 0 !important;
        }

        p, li {
            color: var(--bwdc-teal-deep);
        }

        p {
            max-width: 850px;
            line-height: 1.58;
        }

        div[data-testid="stExpander"] {
            border: 1px solid rgba(41, 73, 67, 0.16) !important;
            border-radius: 10px !important;
            background: rgba(255, 255, 255, 0.48) !important;
            box-shadow: 0 8px 20px rgba(24, 49, 45, 0.035);
            margin: 0.8rem 0 1rem;
        }

        div[data-testid="stExpander"] summary {
            color: var(--bwdc-teal-deep) !important;
            font-weight: 750 !important;
        }

        div[data-testid="stSelectbox"] label,
        div[data-testid="stMultiSelect"] label,
        div[data-testid="stTextInput"] label {
            color: var(--bwdc-teal-deep) !important;
            font-weight: 700 !important;
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

        .section-container {
            margin: 1rem 0 2.4rem;
            padding: 0.35rem 0 0;
        }

        .report-intro {
            border: 1px solid rgba(41, 73, 67, 0.16);
            border-radius: 12px;
            background:
                linear-gradient(135deg, rgba(255, 255, 255, 0.94), rgba(255, 247, 220, 0.78));
            padding: 1.25rem 1.35rem;
            margin: 0.6rem 0 1.5rem;
            box-shadow: 0 14px 32px rgba(24, 49, 45, 0.055);
        }

        .report-intro p {
            max-width: 820px;
            margin: 0;
            font-size: 1.04rem;
            line-height: 1.62;
            color: var(--bwdc-teal-deep);
        }

        .figure-container {
            border: 1px solid rgba(41, 73, 67, 0.18);
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.72);
            padding: 1rem 1.05rem;
            margin: 0.8rem 0 1.3rem;
            box-shadow: 0 14px 30px rgba(24, 49, 45, 0.055);
        }

        .figure-container h3 {
            margin: 0 0 0.25rem;
        }

        .figure-container p,
        .figure-caption {
            color: var(--bwdc-muted);
            font-size: 0.94rem;
            line-height: 1.45;
            margin: 0.25rem 0 0.35rem;
            max-width: 900px;
        }

        .summary-card,
        .profile-card,
        .metric-card,
        .action-tile,
        .link-card,
        .reference-card {
            border: 1px solid rgba(41, 73, 67, 0.15);
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.86);
            box-shadow: 0 10px 24px rgba(24, 49, 45, 0.045);
            transition: transform 150ms ease, box-shadow 150ms ease, border-color 150ms ease;
        }

        .summary-card:hover,
        .profile-card:hover,
        .action-tile:hover,
        .link-card:hover,
        .reference-card:hover {
            transform: translateY(-2px);
            border-color: rgba(41, 73, 67, 0.25);
            box-shadow: 0 16px 30px rgba(24, 49, 45, 0.07);
        }

        .summary-card {
            min-height: 300px;
            padding: 1.05rem;
            background:
                linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(255, 247, 220, 0.58));
        }

        .summary-card h3,
        .profile-card h3,
        .action-tile h3,
        .reference-card h3,
        .link-card h3 {
            margin: 0.45rem 0 0.45rem;
            line-height: 1.25;
        }

        .profile-card {
            min-height: 210px;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.82);
        }

        .profile-card p,
        .summary-card p,
        .action-tile p,
        .reference-card p,
        .link-card p {
            color: var(--bwdc-muted);
            line-height: 1.5;
            margin: 0.35rem 0;
        }

        .evidence-board-card {
            min-height: 360px;
            padding: 1rem;
            border-top: 5px solid var(--bwdc-gold);
        }

        .quote-card {
            border-left: 5px solid var(--bwdc-gold-deep);
            border-radius: 10px;
            background: rgba(255, 247, 220, 0.72);
            padding: 0.78rem 0.9rem;
            margin: 0.5rem 0;
            font-size: 0.98rem;
            line-height: 1.5;
            color: var(--bwdc-teal-deep);
            font-style: italic;
        }

        .quote-card small,
        .quote-source {
            display: block;
            margin-top: 0.4rem;
            color: var(--bwdc-muted);
            font-style: normal;
            font-size: 0.8rem;
            font-weight: 700;
        }

        .metric-card {
            padding: 1rem 1.05rem;
            text-align: left;
            background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(241,247,223,0.62));
        }

        .metric-card .metric-value {
            display: block;
            font-size: 2.35rem;
            line-height: 1;
            font-weight: 850;
            color: var(--bwdc-teal-deep);
            margin: 0.35rem 0;
        }

        .action-tile {
            padding: 1rem;
            min-height: 145px;
            background:
                linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(255, 247, 220, 0.56));
            border-left: 6px solid var(--bwdc-gold-deep);
            margin: 0.35rem 0 0.75rem;
        }

        .action-tile .action-kicker {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            margin-bottom: 0.5rem;
        }

        .action-tile .action-number {
            width: 2.15rem;
            height: 2.15rem;
            border-radius: 999px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: var(--bwdc-teal);
            color: var(--bwdc-cream-soft);
            font-weight: 850;
            box-shadow: inset 0 0 0 2px rgba(255, 250, 240, 0.22);
            flex: 0 0 auto;
        }

        .action-tile .action-summary {
            color: var(--bwdc-muted);
            font-size: 0.95rem;
            line-height: 1.45;
            margin: 0.2rem 0 0.75rem;
        }

        .action-theme-list {
            display: grid;
            gap: 0.48rem;
            margin-top: 0.65rem;
        }

        .action-theme-row {
            border: 1px solid rgba(41, 73, 67, 0.12);
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.68);
            padding: 0.62rem 0.68rem;
        }

        .action-theme-row strong {
            display: block;
            font-size: 0.92rem;
            line-height: 1.28;
            color: var(--bwdc-teal-deep);
            margin-bottom: 0.18rem;
        }

        .action-theme-row span {
            display: block;
            color: var(--bwdc-muted);
            font-size: 0.84rem;
            line-height: 1.36;
        }

        .action-button-note {
            color: var(--bwdc-muted);
            font-size: 0.82rem;
            margin: 0.25rem 0 0.2rem;
        }

        .link-card {
            padding: 0.9rem;
            min-height: 120px;
        }

        .link-card a {
            color: var(--bwdc-teal-deep);
            font-weight: 800;
            text-decoration: none;
        }

        .link-card a:hover {
            text-decoration: underline;
        }

        .reference-card {
            padding: 0.85rem;
            background: rgba(255, 255, 255, 0.72);
        }

        .tag-pill {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 0.2rem 0.58rem;
            background: rgba(215, 232, 189, 0.72);
            border: 1px solid rgba(41, 73, 67, 0.14);
            color: var(--bwdc-teal-deep);
            font-size: 0.76rem;
            font-weight: 750;
            line-height: 1.2;
        }

        .compact-reference-card {
            padding: 0.75rem;
            border-radius: 10px;
            border: 1px solid rgba(41, 73, 67, 0.12);
            background: rgba(255, 250, 240, 0.76);
            margin: 0.45rem 0;
        }

        .soft-card {
            border: 1px solid var(--bwdc-line);
            border-radius: 8px;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.82);
            min-height: 142px;
            box-shadow: 0 10px 30px rgba(24, 49, 45, 0.05);
        }

        .soft-card,
        .evidence-card,
        .central-issue-card,
        .journey-stage-card {
            transition: transform 150ms ease, box-shadow 150ms ease, border-color 150ms ease;
        }

        .soft-card:hover,
        .evidence-card:hover,
        .central-issue-card:hover,
        .journey-stage-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 14px 28px rgba(24, 49, 45, 0.075);
        }

        .soft-card h3 {
            margin-top: 0;
            font-size: 1.05rem;
        }

        .soft-card p {
            color: var(--bwdc-muted);
            line-height: 1.45;
        }

        .rq-card {
            display: flex;
            flex-direction: column;
            min-height: 230px;
        }

        .rq-card h3 {
            margin-top: 0.45rem;
            color: var(--bwdc-teal-deep);
        }

        .rq-card p {
            margin-bottom: 0.55rem;
        }

        .rq-badge {
            display: inline-block;
            align-self: flex-start;
            padding: 0.18rem 0.6rem;
            border-radius: 999px;
            background: var(--bwdc-teal);
            color: var(--bwdc-cream);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
        }

        .takeaway {
            border-left: 5px solid var(--bwdc-sage);
            background: #f1f7df;
            padding: 1rem 1.1rem;
            border-radius: 6px;
            color: var(--bwdc-teal-deep);
        }

        .page-hero {
            display: grid;
            grid-template-columns: minmax(0, 1.05fr) minmax(280px, 0.95fr);
            gap: 1.35rem;
            align-items: stretch;
            margin: 0.7rem 0 2rem;
        }

        .hero-copy {
            border-radius: 8px;
            padding: 1.35rem;
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid var(--bwdc-line);
            box-shadow: 0 14px 34px rgba(24, 49, 45, 0.06);
        }

        .hero-copy h2 {
            margin: 0 0 0.85rem;
            font-size: clamp(1.7rem, 3vw, 2.55rem);
            line-height: 1.08;
        }

        .hero-copy p {
            max-width: 760px;
            line-height: 1.55;
        }

        .hero-visual {
            min-height: 275px;
            border-radius: 8px;
            padding: 1rem;
            border: 1px dashed rgba(41, 73, 67, 0.32);
            background:
                linear-gradient(135deg, rgba(215, 232, 189, 0.74), rgba(255, 247, 220, 0.92)),
                #fffaf0;
            display: grid;
            align-content: end;
            position: relative;
            overflow: hidden;
        }

        .hero-visual::before {
            content: "";
            position: absolute;
            right: 1rem;
            top: 1rem;
            width: 42%;
            height: 42%;
            background:
                linear-gradient(90deg, transparent 30%, rgba(41, 73, 67, 0.12) 31% 34%, transparent 35%),
                linear-gradient(180deg, transparent 45%, rgba(41, 73, 67, 0.14) 46% 50%, transparent 51%),
                rgba(255, 250, 240, 0.75);
            border: 2px solid rgba(41, 73, 67, 0.22);
            border-radius: 6px;
        }

        .hero-visual::after {
            content: "";
            position: absolute;
            left: 1.1rem;
            bottom: 4.8rem;
            width: 38%;
            height: 34%;
            background: var(--bwdc-teal);
            opacity: 0.9;
            clip-path: polygon(50% 0, 100% 34%, 100% 100%, 0 100%, 0 34%);
        }

        .hero-visual h3,
        .hero-visual p {
            position: relative;
            z-index: 1;
        }

        .key-takeaway-card {
            border-left: 6px solid var(--bwdc-gold-deep);
            border-radius: 8px;
            background: rgba(255, 247, 220, 0.86);
            padding: 0.9rem 1rem;
            margin: 0.55rem 0 1.15rem;
        }

        .key-takeaway-card strong {
            display: block;
            margin-bottom: 0.25rem;
        }

        .compact-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
            gap: 0.85rem;
            margin: 0.8rem 0 1.25rem;
        }

        .compact-card {
            border: 1px solid var(--bwdc-line);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.84);
            padding: 0.9rem;
            min-height: 112px;
        }

        .compact-card h3 {
            margin: 0 0 0.35rem;
            font-size: 1rem;
        }

        .compact-card p {
            margin: 0;
            color: var(--bwdc-muted);
            font-size: 0.92rem;
            line-height: 1.42;
        }

        .section-subtitle {
            color: var(--bwdc-muted);
            font-size: 1rem;
            line-height: 1.5;
            margin-top: -0.25rem;
            margin-bottom: 1rem;
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

        .evidence-card {
            border: 1px solid var(--bwdc-line);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.88);
            padding: 0.95rem;
            margin: 0.45rem 0 0.75rem;
            box-shadow: 0 8px 22px rgba(24, 49, 45, 0.045);
        }

        .evidence-card h3,
        .evidence-card h4 {
            margin: 0 0 0.35rem 0;
            font-size: 1.02rem;
            line-height: 1.28;
        }

        .evidence-card p {
            margin: 0.35rem 0;
            line-height: 1.48;
        }

        .evidence-card small,
        .muted-note {
            color: var(--bwdc-muted);
        }

        .mini-quote {
            border-left: 4px solid var(--bwdc-gold);
            padding: 0.35rem 0 0.35rem 0.65rem;
            margin: 0.4rem 0;
            color: var(--bwdc-teal-deep);
            font-size: 0.95rem;
            font-style: italic;
            line-height: 1.42;
            background: rgba(255, 247, 220, 0.58);
        }

        .mini-quote small {
            display: block;
            margin-top: 0.35rem;
            color: var(--bwdc-muted);
            font-style: normal;
            font-size: 0.78rem;
            font-weight: 700;
        }

        .badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.35rem;
            margin: 0.45rem 0;
        }

        .level-badge,
        .type-badge,
        .node-chip {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 0.18rem 0.55rem;
            font-size: 0.76rem;
            font-weight: 700;
            border: 1px solid rgba(24, 49, 45, 0.14);
            line-height: 1.2;
        }

        .type-badge {
            background: var(--bwdc-teal);
            color: #fffaf0;
        }

        .badge-icon {
            margin-right: 0.28rem;
        }

        .node-chip {
            background: #f1f7df;
            color: var(--bwdc-teal-deep);
            font-weight: 600;
        }

        .hierarchy-level {
            border-left: 6px solid var(--level-color, var(--bwdc-sage));
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.7);
            padding: 0.85rem;
            margin: 0.75rem 0 1rem;
        }

        .hierarchy-level h3 {
            margin-top: 0;
        }

        .central-issue-card {
            border: 2px solid #4f8f5b;
            background: #eef7e8;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.8rem 0 1.1rem;
        }

        .detail-panel {
            border: 1px solid rgba(41, 73, 67, 0.24);
            border-radius: 8px;
            background: #fff7dc;
            padding: 1rem;
            margin: 0.7rem 0 1rem;
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

        .journey-figure {
            margin: 0.25rem 0 0.5rem;
        }

        .journey-figure img {
            width: 100%;
            aspect-ratio: 16 / 9;
            object-fit: cover;
            border-radius: 8px;
            border: 1px solid rgba(41, 73, 67, 0.18);
            box-shadow: 0 12px 26px rgba(24, 49, 45, 0.12);
            display: block;
        }

        .journey-figure figcaption {
            margin-top: 0.45rem;
            color: var(--bwdc-muted);
            font-size: 0.9rem;
            line-height: 1.35;
        }

        .journey-image-placeholder {
            min-height: 260px;
            border: 1px dashed rgba(41, 73, 67, 0.34);
            border-radius: 8px;
            background: linear-gradient(135deg, rgba(215, 232, 189, 0.7), rgba(255, 247, 220, 0.9));
            padding: 1rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
        }

        .journey-image-placeholder.hero-placeholder {
            min-height: 320px;
        }

        .journey-stage-card {
            padding: 0.25rem 0 0.45rem;
        }

        .journey-stage-card h3 {
            margin: 0.45rem 0 0.55rem;
            font-size: 1.35rem;
        }

        .journey-stage-card p {
            line-height: 1.55;
        }

        .story-hook {
            font-size: 1.16rem;
            font-weight: 750;
            line-height: 1.38;
            color: var(--bwdc-teal-deep);
            margin: 0.35rem 0 0.55rem;
        }

        .journey-stage-meta,
        .journey-stage-barrier {
            display: grid;
            grid-template-columns: minmax(150px, 0.34fr) 1fr;
            gap: 0.85rem;
            padding: 0.65rem 0;
            border-top: 1px solid rgba(41, 73, 67, 0.12);
            align-items: start;
        }

        .journey-stage-meta strong,
        .journey-stage-barrier strong {
            color: var(--bwdc-teal-deep);
        }

        .journey-stage-meta span,
        .journey-stage-barrier span {
            color: var(--bwdc-muted);
            line-height: 1.42;
        }

        .journey-stage-barrier {
            background: rgba(255, 247, 220, 0.72);
            border-radius: 8px;
            border: 1px solid rgba(239, 194, 103, 0.45);
            padding: 0.72rem;
            margin-top: 0.35rem;
        }

        @media (max-width: 900px) {
            .page-hero {
                grid-template-columns: 1fr;
            }

            .scene-row {
                grid-template-columns: 1fr;
            }

            .scene-step::after {
                right: 50%;
                top: auto;
                bottom: -0.55rem;
                transform: translateX(50%) rotate(135deg);
            }

            .journey-stage-meta,
            .journey-stage-barrier {
                grid-template-columns: 1fr;
                gap: 0.22rem;
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


def section_h2(fragment_id: str, title_plain: str) -> None:
    """Native H2 with a stable DOM id for sidebar TOC links."""
    st.header(title_plain, anchor=fragment_id)


def render_page_toc(page_key: str, sections: tuple[tuple[str, str], ...]) -> None:
    """Render a sidebar table of contents with scroll-position highlighting."""
    if not sections:
        return

    safe_page_key = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in page_key)
    toc_root_id = f"{safe_page_key}-toc-root"
    link_prefix = f"{safe_page_key}-toc-link-"
    cleanup_name = f"__{safe_page_key}TocCleanup"
    targets_name = f"__{safe_page_key}TocScrollTargets"
    resize_name = f"__{safe_page_key}TocResizeHandler"
    link_rows = "".join(
        f'<a id="{link_prefix}{fragment_id}" class="page-toc-item{" toc-active" if idx == 0 else ""}" href="#{fragment_id}">{escape(label)}</a>'
        for idx, (fragment_id, label) in enumerate(sections)
    )
    sections_json = json.dumps([{"id": fragment_id, "label": label} for fragment_id, label in sections])

    with st.sidebar:
        st.markdown(
            f"""
            <style>
                section[data-testid="stMain"] h2 {{
                    scroll-margin-top: 4.5rem;
                }}
                section[data-testid="stSidebar"] #{toc_root_id} {{
                    font-family: inherit;
                    margin: 0.15rem 0 0.9rem 0;
                }}
                section[data-testid="stSidebar"] #{toc_root_id} .page-toc-page-title {{
                    font-size: 1em;
                    font-weight: 600;
                    color: #fffaf0 !important;
                    letter-spacing: 0;
                    margin: 0 0 0.5rem 0;
                    padding: 0;
                    text-decoration: none !important;
                    border: none;
                    box-shadow: none;
                }}
                section[data-testid="stSidebar"] #{toc_root_id} .page-toc-item {{
                    display: block;
                    margin: 0.08rem 0;
                    padding: 0.38rem 0.45rem;
                    border: 2px solid transparent !important;
                    border-radius: 6px;
                    color: rgba(255, 250, 240, 0.92) !important;
                    text-decoration: none !important;
                    font-size: 1em;
                    line-height: inherit;
                    font-weight: 500 !important;
                }}
                section[data-testid="stSidebar"] #{toc_root_id} .page-toc-item:hover {{
                    background: rgba(239, 194, 103, 0.15) !important;
                }}
                section[data-testid="stSidebar"] #{toc_root_id} .page-toc-item.toc-active {{
                    font-weight: 700 !important;
                    color: #fffaf0 !important;
                    border: 2px solid #efc267 !important;
                    background: rgba(0, 0, 0, 0.18) !important;
                }}
            </style>
            <div id="{toc_root_id}">
                <p class="page-toc-page-title">On this page</p>
                {link_rows}
            </div>
            """,
            unsafe_allow_html=True,
        )

    toc_scroll_spy = f"""
    <script>
    (function () {{
        const W = window.parent;
        const doc = W.document;
        const sections = {sections_json};
        const markerSlackPx = 8;

        function getMarkerPx() {{
            const id0 = sections.length ? sections[0].id : "";
            const probe = id0 ? resolveHeading(id0) : null;
            if (!probe) return 100;
            const sm = parseFloat(W.getComputedStyle(probe).scrollMarginTop);
            const base = Number.isFinite(sm) && sm > 0 ? sm : 72;
            return Math.round(base + markerSlackPx);
        }}

        if (typeof W.{cleanup_name} === "function") {{
            try {{ W.{cleanup_name}(); }} catch (e) {{}}
        }}

        function isVerticalScroller(el) {{
            if (!el || el.nodeType !== 1) return false;
            const st = W.getComputedStyle(el);
            const oy = st.overflowY;
            if (oy !== "auto" && oy !== "scroll" && oy !== "overlay") return false;
            return el.scrollHeight > el.clientHeight + 10;
        }}

        function findLargestVerticalScrollerFrom(main) {{
            if (!main) return W;
            let best = W;
            let bestMax = Math.max(0, doc.documentElement.scrollHeight - W.innerHeight);
            const consider = function (el) {{
                if (!isVerticalScroller(el)) return;
                const m = el.scrollHeight - el.clientHeight;
                if (m > bestMax) {{
                    bestMax = m;
                    best = el;
                }}
            }};
            let n = main;
            while (n) {{
                consider(n);
                n = n.parentElement;
            }}
            main.querySelectorAll("*").forEach(consider);
            return best;
        }}

        function resolveHeading(secId) {{
            const main = doc.querySelector('[data-testid="stMain"]');
            if (main) {{
                try {{
                    const idSel = typeof CSS !== "undefined" && CSS.escape ? CSS.escape(secId) : secId;
                    const found = main.querySelector("#" + idSel);
                    if (found) return found;
                }} catch (e) {{}}
            }}
            return doc.getElementById(secId);
        }}

        function setActive(id) {{
            sections.forEach(function (sec) {{
                const link = doc.getElementById("{link_prefix}" + sec.id);
                if (!link) return;
                if (sec.id === id) link.classList.add("toc-active");
                else link.classList.remove("toc-active");
            }});
        }}

        function addScrollAncestors(start, set) {{
            let el = start;
            while (el) {{
                const st = W.getComputedStyle(el);
                const oy = st.overflowY;
                if ((oy === "auto" || oy === "scroll" || oy === "overlay") && el.scrollHeight > el.clientHeight + 2) {{
                    set.add(el);
                }}
                el = el.parentElement;
            }}
        }}

        function gatherScrollTargets() {{
            const targets = new Set();
            targets.add(W);
            const main = doc.querySelector('[data-testid="stMain"]');
            if (main) {{
                const primary = findLargestVerticalScrollerFrom(main);
                if (primary && primary !== W) targets.add(primary);
                addScrollAncestors(main, targets);
            }}
            const app = doc.querySelector('[data-testid="stAppViewContainer"]');
            if (app) addScrollAncestors(app, targets);
            doc.querySelectorAll('[data-testid="stVerticalBlockBorderWrapper"]').forEach(function (el) {{
                const st = W.getComputedStyle(el);
                if ((st.overflowY === "auto" || st.overflowY === "scroll" || st.overflowY === "overlay") &&
                    el.scrollHeight > el.clientHeight + 2) {{
                    targets.add(el);
                }}
            }});
            return Array.from(targets);
        }}

        function computeActive() {{
            const main = doc.querySelector('[data-testid="stMain"]');
            if (!main) {{
                setActive(sections[0].id);
                return;
            }}
            const m = main.getBoundingClientRect();
            const markerPx = getMarkerPx();
            const line = m.top + Math.max(markerPx, Math.round(m.height * 0.26));
            let bestId = sections[0].id;
            let bestTop = -Infinity;
            sections.forEach(function (sec) {{
                const el = resolveHeading(sec.id);
                if (!el) return;
                const top = el.getBoundingClientRect().top;
                if (top > line) return;
                if (top > bestTop) {{
                    bestTop = top;
                    bestId = sec.id;
                }}
            }});
            if (bestTop === -Infinity) bestId = sections[0].id;
            setActive(bestId);
        }}

        let raf = 0;
        function onScrollOrResize() {{
            if (raf) return;
            raf = W.requestAnimationFrame(function () {{
                raf = 0;
                computeActive();
            }});
        }}

        function bind() {{
            const scrollTargets = gatherScrollTargets();
            W.{targets_name} = [];
            scrollTargets.forEach(function (t) {{
                t.addEventListener("scroll", onScrollOrResize, {{ passive: true }});
                W.{targets_name}.push([t, onScrollOrResize]);
            }});
            W.addEventListener("resize", onScrollOrResize, {{ passive: true }});
            W.{resize_name} = onScrollOrResize;
            W.{cleanup_name} = function () {{
                (W.{targets_name} || []).forEach(function (pair) {{
                    pair[0].removeEventListener("scroll", pair[1]);
                }});
                W.{targets_name} = [];
                if (W.{resize_name}) {{
                    W.removeEventListener("resize", W.{resize_name});
                    W.{resize_name} = null;
                }}
                W.{cleanup_name} = null;
            }};
            setTimeout(computeActive, 0);
            setTimeout(computeActive, 250);
            setTimeout(computeActive, 700);
            setTimeout(computeActive, 1500);
        }}

        if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", bind);
        else bind();
    }})();
    </script>
    """
    components.html(toc_scroll_spy, height=1, scrolling=False)
