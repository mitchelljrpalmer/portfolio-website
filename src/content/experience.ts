export type ExperienceEntry = {
  role: string;
  org: string;
  period: string;
  type: string;
  bullets: string[];
  tools?: string[];
};

export const experience: ExperienceEntry[] = [
  {
    role: "Ecommerce & Digital Catalogue Manager",
    org: "Climb On Equipment",
    period: "May 2026 – On Going",
    type: "Contract",
    bullets: [
      "Building an AI-powered product upload pipeline, shifting manual, labour-intensive, error-prone catalog entry to a streamlined, automated workflow.",
      "Building new data flow automations between newly integrated inventory management systems (Prediko ⇌ Shopify) to drive operational efficiency and productivity.",
      "Maintain catalog integrity across 4,000+ technical products and 10,000+ variants for a high-performing ecommerce store, inherited alongside an extensive SOP library.",
      "Manage complex variant architecture, metafields/metaobjects, and bulk catalog operations via Matrixify, including SEO-preserving lifecycle management for discontinued SKUs.",
      "Coordinate associates on catalog workflows and maintain current process documentation."
    ],
    tools: ["Google Workspace App Script", "Google Sheets", "Google Docs", "Shopify", "Matrixify", "Prediko", "AI-Powered Automation", "HTML", "CSS", "Liquid", "Javascript", "Shopify Flow"],
  },
  {
    role: "Data Services Contractor",
    org: "Bella Coola Heli Sports",
    period: "February 2026 – May 2026",
    type: "Fixed Contract",
    bullets: [
      "Established the foundational Single Source of Truth (SSOT) document framework for a limited-hours data infrastructure engagement.",
      "Mapped document lineage and identified priority documents across transportation, rate sheets, and guest-facing guidelines.",
    ],
    tools: ["Google Workspace App Script", "Google Sheets", "Google Docs"],
  },
  {
    role: "Sales & Reservations",
    org: "Bella Coola Heli Sports",
    period: "November 2024 – June 2025",
    type: "Full Time",
    bullets: [
      "Managed bookings valued up to $350,000.",
      "Built automation tools for daily reporting and scheduling, saving ~124 hours per season.",
      "Enhanced customer service coordination.",
      "Extended the scheduling system built during my receptionist role with an automated guest itinerary generator, auto-populating each guest's dated activity itinerary in consumer-facing language (mapped from internal scheduling codes) ready to drop into pre-arrival emails.",
    ],
    tools: ["Salesforce", "Google Sheets"],
  },
  {
    role: "Wildlife Lodge Receptionist",
    org: "Bella Coola Heli Sports / Tweedsmuir Park Lodge",
    period: "June 2024 – October 2024",
    type: "Seasonal",
    bullets: [
      "Coordinated scheduling for guests and guides as the central communication point between operations, hospitality, and guiding teams, while tracking revenue metrics.",
      "Independently built an automated daily schedule generator, producing guide-grouped transit and activity timetables (arrival/departure times, guest counts, destinations) directly from the master Google Sheet, replacing manual schedule-writing and saving ~1 hour/day.",
      "Extended the system with an automated lunch and cooler assignment tool, applying activity-based catering rules by guide and guest count, saving a further ~45 minutes/day.",
      "Built self-initiated, outside formal job duties; the team has since re-engaged me multiple times to refine the tools, and I've virtually trained two cohorts of new staff on them, who reported it significantly eased their onboarding.",
    ],
    tools: ["Google Sheets", "Conditional Logic"],
  },
  {
    role: "Direct-to-Consumer Manager & Logistics Specialist",
    org: "RMU Outdoors",
    period: "June 2020 – December 2023",
    type: "Full Time",
    bullets: [
      "Managed $1.8M product distribution across global channels.",
      "Expanded e-commerce revenue to $500K.",
      "Oversaw inventory and freight workflows across multiple regions.",
    ],
    tools: ["Jira", "Trello", "Google Sheets", "Shipedge", "Klaviyo", "Shopify", "Google Analytics"],
  },
  {
    role: "Various Hospitality Roles",
    org: "Canada & New Zealand",
    period: "2015 – 2020",
    type: "5 years, cumulative",
    bullets: ["Bartending, serving, and guest experience roles across Canada and New Zealand."],
  },
  {
    role: "Basketball Referee",
    org: "North Harbour Basketball / Basketball New Zealand",
    period: "2010 – 2017",
    type: "High School & University",
    bullets: [
      "Officiated competitive basketball from high school through university, progressing to Junior Nationals and the top men's city division.",
      "Built leadership, communication, and decision-making skills under pressure, managing fast-paced games and high-stakes calls in front of players, coaches, and crowds.",
      "Developed composure and clear communication from a young age, officiating alongside adult referees in senior men's competition.",
    ],
  },
];

export const education = [
  { credential: "Data Science Immersive Diploma", org: "Lighthouse Labs", year: "Sep. 2025" },
  { credential: "Advanced Data Analytics – Professional Certificate", org: "Google", year: "2025" },
  { credential: "Data Analytics – Professional Certificate", org: "Google", year: "2024" },
  { credential: "DipGrad – Psychology", org: "", year: "2018" },
  { credential: "BSc – Microbiology & Immunology", org: "", year: "2017" },
];

export const skills = [
  "SQL (PostgreSQL, SQLite)",
  "Excel / Google Sheets",
  "Visualisation Software (Tableau & Tableau Public, Python Plotly)",
  "Python (Pandas, NumPy, Seaborn, Plotly, Scikit-Learn, statsmodels.api, GeoPandas)",
  "Cloud Inventory & Order Management (QuickBooks Commerce, Shopify, Square, Prediko)",
  "E-commerce & Catalog Tools (Shopify, Matrixify, Shopify Flow, Liquid)",
  "CRM Software (Salesforce, Zendesk)",
  "Email Service Provider Software (Klaviyo, Mailchimp)",
  "Coding Languages (HTML, CSS, JavaScript, Google Apps Script, XML, JSON)",
  "Image Segmentation (YOLO)",
  "GIS & Remote Sensing (Google Earth Engine)",
  "Machine Learning Algorithms (Bayes, XGBoost, Regression)",
  "Agile & Project Management Tools (Jira, Trello)",
  "Warehouse & Fulfilment / 3PL Systems (3PL Central/Extensiv, Shipedge)",
  "Collaboration Tools (Teams, Zoom, Google Docs)",
];

export const services = [
  {
    icon: "/images/icons/stats.png",
    title: "Data Analysis & Discovery",
    description:
      "Turn raw data into actionable insights using Python, SQL and statistical analysis. Support strategic decisions, operational improvements, and business growth.",
  },
  {
    icon: "/images/icons/operation.png",
    title: "Operations & Applied Modeling",
    description:
      "Design ML-driven solutions to uncover patterns, optimise workflows, and build predictive models that inform smarter decision-making.",
  },
  {
    icon: "/images/icons/carbon-cloud.png",
    title: "Environmental Data & Impact",
    description:
      "Utilise geospatial and climate data to support resilience planning, environmental forecasting, and sustainability strategy. Bridge business and ecosystems through measurable insight.",
  },
  {
    icon: "/images/icons/paint-brush.png",
    title: "Visual Design & Communication",
    description:
      "Create compelling visual narratives and dashboards for stakeholders that elevate understanding and bring data stories to life.",
  },
  {
    icon: "/images/icons/pipeline.png",
    title: "Pipelines & Efficiencies",
    description:
      "Automate data refreshes and operational workflows so teams spend less time in spreadsheets and more time acting on insights.",
  },
];
