import streamlit as st
import textwrap

TEAM_MEMBERS = [
    {
        "name": "Habibur Rahman Zihad",
        "role": "Founder & Community Director",
        "subRole": "Vision & Strategy Lead",
        "bio": "The visionary behind NagarNirman, driving community engagement and strategic direction. Passionate about leveraging technology to solve civic problems and create meaningful impact across Bangladesh.",
        "image": "https://res.cloudinary.com/dvq3pcykn/image/upload/v1758785330/IMG-20241101-WA0192_vyojiv.jpg",
        "accentColor": "#004d40",
        "skills": ["Leadership", "Community Building", "Strategic Planning", "Project Management"],
        "contributions": ["Project Vision", "Community Outreach", "Team Coordination"],
        "social": {
            "github": "https://github.com/HabiburRahmanZihad",
            "linkedin": "https://linkedin.com/in/habiburrahmanzihad",
            "portfolio": "https://habibur-rahman-zihad.vercel.app/",
            "facebook": "https://www.facebook.com/habiburrahmanzihad.zihad"
        },
        "funFact": "Dreams in code and wakes up with solutions",
        "quote": '\"Together we build, together we rise.\"'
    },
    {
        "name": "Md. Shahariar Hafiz",
        "role": "Co-Founder & Tech Lead",
        "subRole": "Full Stack & Architecture",
        "bio": "The technical mastermind orchestrating the entire NagarNirman ecosystem. Specializes in scalable architecture and cutting-edge development practices that power our civic platform.",
        "image": "https://avatars.githubusercontent.com/u/102473526?v=4",
        "accentColor": "#f2a921",
        "skills": ["Next.js", "Node.js", "MongoDB", "System Architecture"],
        "contributions": ["Core Development", "API Design", "Database Architecture"],
        "social": {
            "github": "https://github.com/mdshahariarhafizofficial",
            "linkedin": "https://www.linkedin.com/in/devshahariarhafiz",
            "portfolio": "https://shahariar-hafiz.netlify.app/",
            "facebook": "https://www.facebook.com/mdshahariarhafizofficial"
        },
        "funFact": "Can debug production issues at 3 AM with eyes closed",
        "quote": '\"Code is poetry, architecture is the symphony.\"'
    },
    {
        "name": "MD Mizanur Malita",
        "role": "Operations Manager",
        "subRole": "Process & Quality Lead",
        "bio": "Ensures seamless operations and maintains the highest quality standards across all NagarNirman processes. Expert in optimizing workflows and delivering exceptional user experiences.",
        "image": "https://avatars.githubusercontent.com/u/193724330?v=4",
        "accentColor": "#00695c",
        "skills": ["Operations", "Quality Assurance", "Process Optimization", "Team Management"],
        "contributions": ["Quality Control", "Process Design", "User Testing"],
        "social": {
            "github": "https://github.com/mizanur2734",
            "linkedin": "https://www.linkedin.com/in/md-mizanur-malita",
            "portfolio": "https://my-portfolio-4wlb.vercel.app/",
            "facebook": "https://www.facebook.com/md.mizanur.rahman.959549"
        },
        "funFact": "Has a sixth sense for catching bugs before they happen",
        "quote": '\"Excellence is not an act, but a habit.\"'
    },
    {
        "name": "Mohammad Bin Amin",
        "role": "Outreach Coordinator",
        "subRole": "Community & Growth Lead",
        "bio": "Bridges the gap between technology and community. Drives user adoption and ensures NagarNirman reaches every corner of Bangladesh through strategic outreach and engagement initiatives.",
        "image": "https://res.cloudinary.com/dfm0bhtyb/image/upload/v1765699151/qmbjzklvweuy3brrnt3v.png",
        "accentColor": "#9c27b0",
        "skills": ["Community Outreach", "Marketing", "User Engagement", "Content Strategy"],
        "contributions": ["User Growth", "Community Building", "Brand Awareness"],
        "social": {
            "github": "https://github.com/Mohammad7558/",
            "linkedin": "https://www.linkedin.com/in/iammohammad",
            "portfolio": "https://iam-mohammad.vercel.app/",
            "facebook": "https://www.facebook.com/imMOHAMMOD/"
        },
        "funFact": "Can convince anyone to try NagarNirman in under 2 minutes",
        "quote": '\"Connection is the key to community transformation.\"'
    }
]


def show_about_page():
    # Hero / Intro block with CTA and quick stats
    hero = textwrap.dedent("""
    <style>
    .about-hero { display:grid; grid-template-columns: 1fr 360px; gap: 24px; align-items: center; padding: 22px; border-radius: 14px; background: linear-gradient(135deg, rgba(34,49,44,0.7), rgba(18,28,24,0.65)); box-shadow: 0 12px 40px rgba(0,0,0,0.6); margin-bottom:18px; }
    .about-hero h1 { margin:0 0 6px 0; font-size:2rem; }
    .about-hero p.lead { margin:0 0 10px 0; opacity:0.95; line-height:1.5; }
    .about-hero .meta { display:flex; gap:12px; align-items:center; }
    .about-hero .stats { display:flex; gap:12px; margin-top:12px; }
    .about-hero .stat { padding:8px 12px; background: rgba(255,255,255,0.03); border-radius:10px; font-weight:700; }
    .about-hero .cta { margin-top:14px; }
    @media (max-width:880px) { .about-hero { grid-template-columns: 1fr; } .about-hero .right { order: -1; margin-bottom:8px;} }
    </style>

    <div class="about-hero">
        <div class="left">
            <h1>About NagarNirman</h1>
            <p class="lead">NagarNirman empowers citizens to report, track, and resolve urban issues collaboratively. We combine community action with practical technology to make cities safer, cleaner, and more responsive.</p>
            <div style="display:flex; gap:18px; flex-wrap:wrap;">
                <div style="min-width:220px;">
                    <b>Mission</b>
                    <div>Connect citizens, community leaders and local authorities to identify and resolve civic problems faster.</div>
                </div>
                <div style="min-width:220px;">
                    <b>Vision</b>
                    <div>Resilient, transparent urban communities powered by people and data.</div>
                </div>
            </div>
            <div class="stats">
                <div class="stat">2,450+ reports</div>
                <div class="stat">12 districts</div>
                <div class="stat">180+ volunteers</div>
            </div>
            <div class="cta"><a href="mailto:hello@nagar-nirman.org" style="background:var(--color-accent); color:#07211a; padding:8px 14px; border-radius:8px; font-weight:700; text-decoration:none;">Join & Support</a></div>
        </div>
        <div class="right">
            <div style="padding:12px; border-radius:12px; background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));">
                <div style="font-size:0.95rem; font-weight:700; margin-bottom:6px;">Our Approach</div>
                <div style="font-size:0.9rem; opacity:0.9;">Community reporting → Volunteer triage → Admin action → Public resolution & analytics.</div>
            </div>
        </div>
    </div>
    """)

    st.markdown(hero, unsafe_allow_html=True)

    st.markdown(textwrap.dedent("""
    **History & Milestones**

    - Founded in 2025, December as a grassroots initiative to aggregate local civic issues and accelerate resolution.
    - 2025: Pilot launched across three districts, with community volunteers and local leaders onboarded.
    - 2026: Platform features expanded to include heatmaps, reporting analytics, and automated PDF reporting for administrators.

    **How It Works**

    1. A citizen files a report with a title, description, and optional photo.
    2. The report is stored in the community database and visible to local volunteers.
    3. Administrators and volunteers triage reports, assign owners, and track status updates.
    4. Resolved reports are archived with timelines and resolution notes for transparency.

    **Core Values**

    - Community-first: People and their lived experience drive our priorities.
    - Transparency: Open reporting and clear status tracking.
    - Practicality: Build tools that help people act and measure impact.
    - Inclusion: Ensure accessibility and reach across diverse communities.

    **Quick Impact Metrics (sample)**

    - Reports submitted: 2,450+
    - Districts active: 12
    - Volunteer contributors: 180+

    """))

    st.header("Meet the Team")

    # Build a single responsive HTML grid (4 columns on wide screens)
    style = textwrap.dedent("""
    <style>
    .about-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 12px; }
    .about-card { padding: 20px; border-radius: 14px; min-height: 340px; display:flex; flex-direction:column; gap:12px; color: var(--text-primary); background: linear-gradient(180deg, rgba(255,255,255,0.015), rgba(0,0,0,0.02)); border: 1px solid rgba(255,255,255,0.04); box-shadow: 0 12px 36px rgba(0,0,0,0.55); transition: transform .28s cubic-bezier(.2,.9,.3,1), box-shadow .28s; overflow: hidden; position: relative; }
    .about-card::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(0,0,0,0.02)); pointer-events: none; }
    .about-card:hover { transform: translateY(-12px) scale(1.02); box-shadow: 0 28px 70px rgba(0,0,0,0.7); }
    .about-card .meta { display:flex; gap:18px; align-items:center; }
    .about-card img { width:140px; height:140px; object-fit:cover; border-radius:12px; border:4px solid rgba(255,255,255,0.06); box-shadow: 0 12px 34px rgba(0,0,0,0.55); transition: transform .28s ease, box-shadow .28s ease; }
    .about-card:hover img { transform: rotate(-3deg) scale(1.03); }
    .about-card .name { font-weight:900; font-size:1.12rem; letter-spacing:0.2px; }
    .about-card .role { font-size:0.9rem; opacity:0.95; }
    .about-card .subrole { font-size:0.78rem; opacity:0.78; }
    .about-card .bio { margin-top:10px; font-size:0.96rem; line-height:1.45; opacity:0.96; }
    .about-card .skills { margin-top:10px; font-size:0.9rem; opacity:0.95; }
    .about-card .links { margin-top:10px; }
    .about-card .links a { color: var(--color-accent, #9ad83e); text-decoration: none; margin-right: 12px; font-weight:700; }
    @media (max-width: 1100px) { .about-grid { grid-template-columns: repeat(3, 1fr); } }
    @media (max-width: 820px) { .about-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 480px) { .about-grid { grid-template-columns: repeat(1, 1fr); } }
    </style>
    """)

    cards = [style, '<div class="about-grid">']
    for member in TEAM_MEMBERS:
        grad = f"linear-gradient(135deg, {member['accentColor']}22, rgba(0,0,0,0.05))"
        card_html = f"""
        <div class="about-card" style="background: {grad}; border-left: 6px solid {member['accentColor']}; padding-left: 14px;">
            <div class="meta">
                <img src="{member['image']}" alt="{member['name']}">
                <div>
                    <div class="name">{member['name']}</div>
                    <div class="role">{member['role']}</div>
                    <div class="subrole">{member['subRole']}</div>
                </div>
            </div>
            <div class="bio">{member['bio']}</div>
            <div class="skills"><b>Skills:</b> {', '.join(member['skills'])}</div>
            <div class="links">
                <a href="{member['social'].get('linkedin', '#')}" target="_blank">LinkedIn</a>
                <a href="{member['social'].get('github', '#')}" target="_blank">GitHub</a>
                <a href="{member['social'].get('portfolio', '#')}" target="_blank">Portfolio</a>
            </div>
        </div>
        """
        cards.append(textwrap.dedent(card_html).strip())
    cards.append('</div>')

    st.markdown('\n'.join(cards), unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Our Impact")
    st.markdown("""
    - Reports processed: *community-driven and growing*
    - Active volunteers: *expanding network across districts*
    """)

    st.info("Want to join the team or contribute? Reach out via LinkedIn or our contact channels.")
