// Agent Database with Live Cloud Run Endpoints
// This file contains all agent data for the philhills.ai agents page

const agents = [
    // NEW ADK AGENTS - WORKING NOW
    {
        name: 'SimpleBot',
        role: 'General Purpose AI Assistant',
        department: 'operations',
        description: 'Working ADK agent powered by Gemini 2.0 Flash. Handles general queries, GCP resource management, and agent orchestration. Successfully tested with live API.',
        capabilities: ['Natural language chat', 'GCP resource queries', 'Task delegation', 'Real-time responses'],
        type: 'adk',
        online: true,
        endpoint: 'http://localhost:8090', // Cloud Run URL will update after deployment
        devUI: 'http://localhost:8090/dev-ui/?app=app'
    },
    {
        name: 'Unified Orchestrator',
        role: 'Multi-Cloud Service Coordinator',
        department: 'operations',
        description: 'Master orchestrator with A2A connections to all 35 Cloud Run services. Delegates tasks intelligently across the entire service mesh.',
        capabilities: ['A2A protocol coordination', '35 Cloud Run services', 'Intelligent task routing', 'Load balancing'],
        type: 'adk',
        online: true,
        endpoint: 'http://localhost:8090', // Local testing
        devUI: 'http://localhost:8090/dev-ui/?app=app'
    },

    // OPERATIONS
    {
        name: 'Orchestrator',
        role: 'LLM-Driven Multi-Agent Coordinator',
        department: 'operations',
        description: 'Main brain using Gemini 2.5 Flash for intelligent task delegation. Coordinates all sub-agents autonomously using LLM decision-making.',
        capabilities: ['Intelligent delegation to 6+ sub-agents', 'Multi-step workflow coordination', 'Error handling and recovery', 'Autonomous problem solving'],
        type: 'adk',
        online: true,
        endpoint: 'https://agentic-orchestrator-768405504263.us-central1.run.app'
    },
    {
        name: 'GCP Expert Admin',
        role: 'Cloud Platform Master (7 Certifications)',
        department: 'engineering',
        description: 'Expert-level GCP administrator with knowledge from all 7 professional certifications. Handles Cloud Run, Vertex AI, Storage, BigQuery, IAM, security, and cost optimization via Cube Protocol.',
        capabilities: ['Deploy to Cloud Run', 'Deploy to Vertex AI Agent Engine', 'IAM security audits', 'Cost optimization (30-50% savings)', 'BigQuery analytics', 'Cube Protocol orchestration'],
        type: 'adk',
        online: true,
        endpoint: 'https://cube-builder-768405504263.us-central1.run.app'
    },
    {
        name: 'Manager Agent',
        role: 'CEO / System Orchestrator',
        department: 'operations',
        description: 'Universal Nexus for the Phil Hills Agentic Empire. Oversees Identity, Revenue, Reputation, and Operations.',
        capabilities: ['Health checks every 15 minutes', 'Task delegation to specialists', 'System-wide coordination'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Backup Agent',
        role: 'Data Safety Net',
        department: 'operations',
        description: 'Syncs critical data to Google Cloud Storage with verification and recovery testing.',
        capabilities: ['Daily backups to GCS', 'Backup verification', 'Recovery testing'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Update Agent',
        role: 'System Maintenance',
        department: 'operations',
        description: 'Monitors dependencies, checks for security patches, and provides update recommendations.',
        capabilities: ['Dependency checks daily', 'Security patch detection', 'Update recommendations'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Architect Agent',
        role: 'System Visualizer',
        department: 'operations',
        description: 'Visualizes the agent mesh, maintains system census, and maps data flows.',
        capabilities: ['Dashboard updates every 6 hours', 'System census', 'Data flow mapping'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Protocol Agent',
        role: 'Compliance Officer',
        department: 'operations',
        description: 'A2A Auditor. Validates CUBE protocol compliance and generates violation alerts.',
        capabilities: ['Message validation continuous', 'Compliance reporting hourly', 'Violation alerts'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Research Agent',
        role: 'The Auditor',
        department: 'operations',
        description: 'Continuous agent auditing and improvement. Verifies role clarity and suggests improvements.',
        capabilities: ['Agent audits every 6 hours', 'Role clarity verification', 'Improvement suggestions'],
        type: 'legacy',
        online: true
    },

    // ENGINEERING
    {
        name: 'GitHub Monitor',
        role: 'Deployment Diagnostician',
        department: 'engineering',
        description: 'Monitors GitHub repositories, Actions workflows, and Pages deployments. Provides diagnostics for deployment failures.',
        capabilities: ['GitHub Actions monitoring', 'Pages deployment diagnostics', 'Workflow failure analysis'],
        type: 'adk',
        online: false // Will be deployed next
    },
    {
        name: 'Deployment Fixer',
        role: 'Autonomous Troubleshooter',
        department: 'engineering',
        description: 'Autonomous deployment issue fixer. Analyzes errors and implements fixes for GitHub Pages and Cloud deployments.',
        capabilities: ['Auto-fix CNAME issues', 'Create .nojekyll files', 'Branch configuration', 'Git commit and push'],
        type: 'adk',
        online: false // Will be deployed next
    },
    {
        name: 'GitHub Admin',
        role: 'VP of Engineering',
        department: 'engineering',
        description: 'Manages 190+ GitHub repositories with CI/CD monitoring and sub-agent spawning capabilities.',
        capabilities: ['CI/CD monitoring hourly', '190+ repos managed', 'Sub-agent spawning (max 50)'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Website Builder',
        role: 'Full-Stack Web Developer',
        department: 'engineering',
        description: 'Orchestrates content generation, deployment, and SEO for philhills.com and philhills.ai.',
        capabilities: ['Content generation', 'Git deployment', 'SEO optimization', 'CUBE protocol integration'],
        type: 'adk',
        online: false // Will be deployed next
    },
    {
        name: 'Site Reliability',
        role: 'Link Integrity Guardian',
        department: 'engineering',
        description: 'Ensures all external links and internal references remain valid across deployed sites.',
        capabilities: ['Link checking', 'Health monitoring', 'Automated fixes'],
        type: 'legacy',
        online: true
    },

    // REVENUE
    {
        name: 'Money Agent',
        role: 'Chief Revenue Officer',
        department: 'revenue',
        description: 'CRO. Audits repositories for revenue opportunities and tracks ROI.',
        capabilities: ['Revenue scans every 6 hours', 'Monetization analysis', 'ROI tracking'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Stripe Agent',
        role: 'Chief Financial Officer',
        department: 'revenue',
        description: 'Revenue automation with Stripe. Handles collection and distribution.',
        capabilities: ['Revenue collection daily 3 AM', 'Revenue distribution', 'Balance monitoring'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Bill Payment Agent',
        role: 'Accounts Payable',
        department: 'revenue',
        description: 'Automated bill payment with scheduling and confirmation.',
        capabilities: ['Bill checks daily 9 AM', 'Automated payment execution', 'Payment confirmation'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Salesforce Admin',
        role: 'CRM Manager',
        department: 'revenue',
        description: 'Manages Salesforce CRM: creates leads, assigns tasks, and posts updates.',
        capabilities: ['Lead creation', 'Task assignment', 'CRM updates'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Industry Pipeline',
        role: 'Lead Generation Orchestrator',
        department: 'revenue',
        description: 'Orchestrates the industry lead gen pipeline: Monitor → Generate → Publish.',
        capabilities: ['Rate monitoring', 'Content generation', 'Auto-publishing'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Industry Rate Monitor',
        role: 'Rate Tracker',
        department: 'revenue',
        description: 'Tracks market rates and detects drops.',
        capabilities: ['Real-time rate tracking', 'Drop detection', 'Alert generation'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Restricted Content Generator',
        role: 'Persuasive Writer',
        department: 'revenue',
        description: "Analyzes rates and trends for restricted industry queries (sanitized).",
        capabilities: ['Persuasive writing', 'CTA optimization', 'Rate analysis'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Industry Cube Publisher',
        role: 'Vertical Publisher',
        department: 'revenue',
        description: 'Publishes signed Identity Cubes to philhills_ai_site/industry/',
        capabilities: ['Industry-specific cubes', 'Lead page generation', 'Catalog updates'],
        type: 'legacy',
        online: true
    },
    {
        name: 'WA Housing Market',
        role: 'Real Estate Data Provider',
        department: 'revenue',
        description: 'Provides real estate market data for Washington State cities (Seattle, Bellevue, Tacoma, etc.).',
        capabilities: ['Market data queries', 'City-specific stats', 'Trend analysis'],
        type: 'legacy',
        online: true
    },

    // DEFENSE
    {
        name: 'Reputation Agent',
        role: 'The Defender',
        department: 'defense',
        description: 'Research & Defense. Monitors identity, detects threats, and deploys Truth Cubes via Social Swarm.',
        capabilities: ['Identity scans every 6 hours', 'Threat detection', 'Truth Cube deployment to Social Swarm'],
        type: 'legacy',
        online: true
    },

    // DISTRIBUTION
    {
        name: 'Media Factory',
        role: 'Content Studio',
        department: 'distribution',
        description: 'Video/Avatar Creation & Trend Analysis. Generates viral content and cubes trending topics.',
        capabilities: ['Trend analysis every 12 hours', 'Avatar video generation', 'Viral content cubing'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Social Swarm',
        role: '7-Platform Distribution Network',
        department: 'distribution',
        description: 'Manages presence across Reddit, TikTok, YouTube, Facebook, Instagram, WhatsApp, and X (Twitter).',
        capabilities: ['7 platform agents', 'Daily content posting 10 AM', 'Cross-platform coordination'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Google Trends Agent',
        role: 'Trend Intelligence',
        department: 'distribution',
        description: 'Queries Google Trends data using BigQuery. Tracks search trends, rising topics, and regional interest.',
        capabilities: ['BigQuery trend queries', 'Rising topic detection', 'Regional analysis'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Trend Pipeline',
        role: 'Content Automation',
        department: 'distribution',
        description: 'Automates the trend-to-cube content generation pipeline. Fetches trends, generates summaries, publishes cubes.',
        capabilities: ['Automated trend fetching', 'AI summary generation', 'Cube publishing'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Cube Publisher',
        role: 'Identity Cube Manager',
        department: 'distribution',
        description: 'Publishes Identity Cubes to philh ills.ai and maintains the cube catalog.',
        capabilities: ['Cube publishing', 'Catalog maintenance', 'Signature verification'],
        type: 'legacy',
        online: true
    },
    {
        name: 'Content Generator',
        role: 'AI Content Writer',
        department: 'distribution',
        description: 'Generates AI summaries for trending topics with backlinks to Phil Hills\' sites.',
        capabilities: ['Trend summarization', 'SEO-optimized content', 'Backlink integration'],
        type: 'legacy',
        online: true
    }
];
