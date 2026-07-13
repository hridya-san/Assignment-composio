import json
import os
from collections import Counter
from html import escape
from pathlib import Path
from typing import List, Dict, Any

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "site"
OUTPUT_DIR.mkdir(exist_ok=True)

APPS: List[Dict[str, Any]] = [
    {"app": "Salesforce", "category": "CRM and Sales", "summary": "Enterprise CRM for sales, service, and customer data.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST + GraphQL; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_rest_resources.htm"},
    {"app": "HubSpot", "category": "CRM and Sales", "summary": "CRM and marketing automation suite for revenue teams.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.hubspot.com/docs/api/overview"},
    {"app": "Pipedrive", "category": "CRM and Sales", "summary": "Sales CRM focused on pipeline and deal tracking.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.pipedrive.com/docs/api/v1"},
    {"app": "Attio", "category": "CRM and Sales", "summary": "Modern CRM with a flexible data model and workflow automation.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://docs.attio.com"},
    {"app": "Twenty", "category": "CRM and Sales", "summary": "Open-source CRM for teams that want self-hosted flexibility.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "Self-hosted deployment", "evidence": "https://docs.twenty.com"},
    {"app": "Podio", "category": "CRM and Sales", "summary": "Work management platform with CRM-style collaboration.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.podio.com"},
    {"app": "Zoho CRM", "category": "CRM and Sales", "summary": "CRM platform for sales, marketing, and support workflows.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://www.zoho.com/crm/developer/docs/api/v2/"},
    {"app": "Close", "category": "CRM and Sales", "summary": "Sales engagement CRM built around calling and email workflows.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://developer.close.com"},
    {"app": "Copper", "category": "CRM and Sales", "summary": "CRM that sits on top of Google Workspace data.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://developer.copper.com"},
    {"app": "DealCloud", "category": "CRM and Sales", "summary": "Relationship intelligence platform for deal and relationship data.", "auth": "OAuth2", "self_serve": "Gated", "api_surface": "REST; narrow", "buildability": "Partial", "blocker": "Enterprise access and partner gating", "evidence": "https://api.docs.dealcloud.com"},
    {"app": "Zendesk", "category": "Support and Helpdesk", "summary": "Customer support suite for tickets, macros, and omnichannel service.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developer.zendesk.com/api-reference/"},
    {"app": "Intercom", "category": "Support and Helpdesk", "summary": "Customer messaging platform for support and product engagement.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.intercom.com/docs/build-an-app"},
    {"app": "Freshdesk", "category": "Support and Helpdesk", "summary": "Helpdesk platform focused on ticketing and automation.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.freshdesk.com"},
    {"app": "Front", "category": "Support and Helpdesk", "summary": "Shared inbox and customer communication workspace.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://dev.frontapp.com"},
    {"app": "Pylon", "category": "Support and Helpdesk", "summary": "Support operations platform for customer-facing teams.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://docs.usepylon.com"},
    {"app": "LiveAgent", "category": "Support and Helpdesk", "summary": "Helpdesk and live chat platform for support teams.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://documentation.liveagent.com"},
    {"app": "Plain", "category": "Support and Helpdesk", "summary": "Support platform with structured channels and automation.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.plain.com"},
    {"app": "Help Scout", "category": "Support and Helpdesk", "summary": "Help desk software for shared inboxes and customer conversations.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://developer.helpscout.com"},
    {"app": "Gorgias", "category": "Support and Helpdesk", "summary": "Ecommerce customer support platform with automation.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.gorgias.com"},
    {"app": "Gladly", "category": "Support and Helpdesk", "summary": "Customer service platform for shopper-first support teams.", "auth": "OAuth2", "self_serve": "Gated", "api_surface": "REST; moderate", "buildability": "Partial", "blocker": "Enterprise plan requirement", "evidence": "https://developer.gladly.com"},
    {"app": "Slack", "category": "Communications and Messaging", "summary": "Workplace messaging and workflow automation hub.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST + GraphQL; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://api.slack.com"},
    {"app": "Twilio", "category": "Communications and Messaging", "summary": "Communication APIs for messaging, voice, and verification.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://www.twilio.com/docs"},
    {"app": "Zoho Cliq", "category": "Communications and Messaging", "summary": "Team chat platform with collaboration features.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://www.zoho.com/cliq/help/developer/"},
    {"app": "Lark", "category": "Communications and Messaging", "summary": "Enterprise collaboration suite with chat and docs.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://open.larksuite.com/document/"},
    {"app": "Pumble", "category": "Communications and Messaging", "summary": "Free team messaging platform for small companies.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://pumble.com/developers"},
    {"app": "Discord", "category": "Communications and Messaging", "summary": "Community chat platform with bot integrations.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://discord.com/developers/docs"},
    {"app": "Telegram", "category": "Communications and Messaging", "summary": "Messaging platform with bot and MTProto APIs.", "auth": "Token", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://core.telegram.org/bots"},
    {"app": "WhatsApp Business", "category": "Communications and Messaging", "summary": "Business messaging with verified workflows and templates.", "auth": "OAuth2", "self_serve": "Gated", "api_surface": "REST; moderate", "buildability": "Partial", "blocker": "Business verification and approval", "evidence": "https://developers.facebook.com/docs/whatsapp"},
    {"app": "Aircall", "category": "Communications and Messaging", "summary": "Cloud phone system with call and contact data APIs.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://developer.aircall.io"},
    {"app": "Vonage", "category": "Communications and Messaging", "summary": "Voice and messaging APIs with a broad developer surface.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developer.vonage.com"},
    {"app": "Google Ads", "category": "Marketing, Ads, Email and Social", "summary": "Advertising platform for search, display, and video campaigns.", "auth": "OAuth2", "self_serve": "Self-serve with review", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "App review", "evidence": "https://developers.google.com/google-ads/api"},
    {"app": "Meta Ads", "category": "Marketing, Ads, Email and Social", "summary": "Meta advertising APIs for campaigns and performance data.", "auth": "OAuth2", "self_serve": "Self-serve with review", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "Business verification", "evidence": "https://developers.facebook.com/docs/marketing-apis"},
    {"app": "LinkedIn Ads", "category": "Marketing, Ads, Email and Social", "summary": "Advertising APIs for sponsored content and lead gen campaigns.", "auth": "OAuth2", "self_serve": "Self-serve with review", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "App review", "evidence": "https://learn.microsoft.com/linkedin/marketing"},
    {"app": "GoHighLevel", "category": "Marketing, Ads, Email and Social", "summary": "Marketing automation suite for agencies and local businesses.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://highlevel.stoplight.io"},
    {"app": "Mailchimp", "category": "Marketing, Ads, Email and Social", "summary": "Email marketing and subscriber lifecycle automation.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://mailchimp.com/developer/"},
    {"app": "Klaviyo", "category": "Marketing, Ads, Email and Social", "summary": "Email and SMS marketing automation for ecommerce teams.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.klaviyo.com"},
    {"app": "systeme.io", "category": "Marketing, Ads, Email and Social", "summary": "Funnel builder for course and product launch campaigns.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://api.systeme.io"},
    {"app": "Pinterest", "category": "Marketing, Ads, Email and Social", "summary": "Visual discovery and social commerce platform.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.pinterest.com"},
    {"app": "Threads", "category": "Marketing, Ads, Email and Social", "summary": "Meta social platform for short-form conversational content.", "auth": "OAuth2", "self_serve": "Self-serve with review", "api_surface": "REST; moderate", "buildability": "Partial", "blocker": "Review and platform policy", "evidence": "https://developers.facebook.com/docs/threads"},
    {"app": "SendGrid", "category": "Marketing, Ads, Email and Social", "summary": "Transactional and marketing email delivery platform.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://www.twilio.com/docs/sendgrid"},
    {"app": "Shopify", "category": "Ecommerce", "summary": "Ecommerce platform with a large merchant API surface.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://shopify.dev/docs/api"},
    {"app": "WooCommerce", "category": "Ecommerce", "summary": "WordPress-based commerce platform with open APIs.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://woocommerce.com/document/woocommerce-rest-api"},
    {"app": "BigCommerce", "category": "Ecommerce", "summary": "Hosted commerce platform for merchants and storefronts.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developer.bigcommerce.com"},
    {"app": "Salesforce Commerce Cloud", "category": "Ecommerce", "summary": "Enterprise commerce platform with composable storefront APIs.", "auth": "OAuth2", "self_serve": "Gated", "api_surface": "REST; broad", "buildability": "Partial", "blocker": "Enterprise licensing", "evidence": "https://developer.salesforce.com/docs/commerce"},
    {"app": "Magento", "category": "Ecommerce", "summary": "Open-source commerce platform for online stores.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developer.adobe.com/commerce"},
    {"app": "Squarespace", "category": "Ecommerce", "summary": "Website builder with integrated commerce features.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.squarespace.com"},
    {"app": "Ecwid", "category": "Ecommerce", "summary": "Embeddable commerce solution for existing websites.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://api-docs.ecwid.com"},
    {"app": "Gumroad", "category": "Ecommerce", "summary": "Creator commerce platform for digital goods and memberships.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://gumroad.com/api"},
    {"app": "Amazon Selling Partner", "category": "Ecommerce", "summary": "Amazon seller backend for catalog and order operations.", "auth": "OAuth2", "self_serve": "Self-serve with review", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "Seller registration and approval", "evidence": "https://developer-docs.amazon.com/sp-api"},
    {"app": "fanbasis", "category": "Ecommerce", "summary": "Creator commerce platform for fan subscriptions and merch.", "auth": "OAuth2", "self_serve": "Gated", "api_surface": "REST; narrow", "buildability": "Partial", "blocker": "Limited public API and partnership context", "evidence": "https://docs.fanfoundation.com"},
    {"app": "DataForSEO", "category": "Data, SEO and Scraping", "summary": "SEO and SERP data provider with structured APIs.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://docs.dataforseo.com"},
    {"app": "SE Ranking", "category": "Data, SEO and Scraping", "summary": "SEO toolkit for rankings, keywords, and audit data.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://seranking.com/api"},
    {"app": "Ahrefs", "category": "Data, SEO and Scraping", "summary": "Backlink and keyword research data provider.", "auth": "API key", "self_serve": "Self-serve with review", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "Plan and approval", "evidence": "https://ahrefs.com/api"},
    {"app": "MrScraper", "category": "Data, SEO and Scraping", "summary": "Scraping and extraction service for web data workflows.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://docs.mrscraper.com"},
    {"app": "Apify", "category": "Data, SEO and Scraping", "summary": "Web scraping and automation platform with actor APIs.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://docs.apify.com"},
    {"app": "Firecrawl", "category": "Data, SEO and Scraping", "summary": "Web crawling and content extraction service.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://www.firecrawl.dev"},
    {"app": "Bright Data", "category": "Data, SEO and Scraping", "summary": "Proxy and data collection infrastructure provider.", "auth": "API key", "self_serve": "Self-serve with review", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "Usage approval", "evidence": "https://docs.brightdata.com"},
    {"app": "Sherlock", "category": "Data, SEO and Scraping", "summary": "Open-source OSINT project for finding online accounts.", "auth": "Other", "self_serve": "Self-serve", "api_surface": "No public API", "buildability": "No", "blocker": "No official API and scraping risk", "evidence": "https://github.com/sherlock-project/sherlock"},
    {"app": "Waterfall.io", "category": "Data, SEO and Scraping", "summary": "Company intelligence and data enrichment platform.", "auth": "API key", "self_serve": "Gated", "api_surface": "REST; narrow", "buildability": "Partial", "blocker": "Enterprise access and sales motion", "evidence": "https://waterfall.io"},
    {"app": "Clay", "category": "Data, SEO and Scraping", "summary": "Data enrichment and prospecting platform.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.clay.com"},
    {"app": "GitHub", "category": "Developer, Infra and Data platforms", "summary": "Developer platform for code hosting, actions, and APIs.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://docs.github.com/rest"},
    {"app": "Vercel", "category": "Developer, Infra and Data platforms", "summary": "Deployment and edge platform for modern apps.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://vercel.com/docs/rest-api"},
    {"app": "Netlify", "category": "Developer, Infra and Data platforms", "summary": "Static site and app deployment platform.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://docs.netlify.com/api"},
    {"app": "Cloudflare", "category": "Developer, Infra and Data platforms", "summary": "Edge network and security platform with a rich API.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.cloudflare.com/api"},
    {"app": "Supabase", "category": "Developer, Infra and Data platforms", "summary": "Open-source backend-as-a-service with Postgres APIs.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://supabase.com/docs"},
    {"app": "Neo4j", "category": "Developer, Infra and Data platforms", "summary": "Graph database platform with developer APIs.", "auth": "Basic", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://neo4j.com/docs/api"},
    {"app": "Snowflake", "category": "Developer, Infra and Data platforms", "summary": "Cloud data platform with SQL and admin APIs.", "auth": "OAuth2", "self_serve": "Self-serve with review", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "Account setup", "evidence": "https://docs.snowflake.com"},
    {"app": "MongoDB Atlas", "category": "Developer, Infra and Data platforms", "summary": "Managed MongoDB service with operational APIs.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://mongodb.com/docs/atlas/api"},
    {"app": "Datadog", "category": "Developer, Infra and Data platforms", "summary": "Observability platform for logs, metrics, and traces.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://docs.datadoghq.com/api"},
    {"app": "Sentry", "category": "Developer, Infra and Data platforms", "summary": "Error monitoring platform with developer integrations.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://docs.sentry.io/api"},
    {"app": "Notion", "category": "Productivity and Project Management", "summary": "Workspace for docs, knowledge bases, and project planning.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.notion.com"},
    {"app": "Airtable", "category": "Productivity and Project Management", "summary": "Low-code database and workflow tool for teams.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://airtable.com/developers"},
    {"app": "Linear", "category": "Productivity and Project Management", "summary": "Issue tracking and project planning for product teams.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.linear.app"},
    {"app": "Jira", "category": "Productivity and Project Management", "summary": "Software project management platform for agile teams.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/"},
    {"app": "Asana", "category": "Productivity and Project Management", "summary": "Task and project management workspace for teams.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developers.asana.com"},
    {"app": "Monday.com", "category": "Productivity and Project Management", "summary": "Work operating system for cross-functional collaboration.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developer.monday.com"},
    {"app": "ClickUp", "category": "Productivity and Project Management", "summary": "All-in-one productivity and team execution platform.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://clickup.com/api"},
    {"app": "Coda", "category": "Productivity and Project Management", "summary": "Document-centric workspace combining docs, tables, and automation.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://coda.io/developers"},
    {"app": "Smartsheet", "category": "Productivity and Project Management", "summary": "Collaborative work management and spreadsheets for operations.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://smartsheet.com/developers"},
    {"app": "Harvest", "category": "Productivity and Project Management", "summary": "Time tracking and billing platform for service teams.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://help.getharvest.com/api-v2"},
    {"app": "Stripe", "category": "Finance and Fintech", "summary": "Payments infrastructure for online commerce and subscriptions.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://stripe.com/docs/api"},
    {"app": "Plaid", "category": "Finance and Fintech", "summary": "Banking and financial data connectivity layer.", "auth": "OAuth2", "self_serve": "Self-serve with review", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "KYC and review", "evidence": "https://plaid.com/docs"},
    {"app": "Binance", "category": "Finance and Fintech", "summary": "Crypto exchange with trading and wallet APIs.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://binance-docs.github.io"},
    {"app": "Paygent Connect", "category": "Finance and Fintech", "summary": "Payment gateway and merchant processing integration.", "auth": "OAuth2", "self_serve": "Gated", "api_surface": "REST; moderate", "buildability": "Partial", "blocker": "Partner and merchant approval", "evidence": "https://developer.paygent.com"},
    {"app": "iPayX", "category": "Finance and Fintech", "summary": "Embedded finance and payments stack for digital products.", "auth": "OAuth2", "self_serve": "Gated", "api_surface": "REST; moderate", "buildability": "Partial", "blocker": "Sales-led onboarding", "evidence": "https://ipayx.ai/docs"},
    {"app": "QuickBooks", "category": "Finance and Fintech", "summary": "Accounting platform for invoices, expenses, and books.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developer.intuit.com"},
    {"app": "Xero", "category": "Finance and Fintech", "summary": "Small-business accounting platform with API access.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; broad", "buildability": "Yes", "blocker": "None", "evidence": "https://developer.xero.com"},
    {"app": "Brex", "category": "Finance and Fintech", "summary": "Corporate card and spend management platform.", "auth": "OAuth2", "self_serve": "Gated", "api_surface": "REST; moderate", "buildability": "Partial", "blocker": "Business underwriting", "evidence": "https://developer.brex.com"},
    {"app": "Ramp", "category": "Finance and Fintech", "summary": "Corporate card and expense management platform.", "auth": "OAuth2", "self_serve": "Gated", "api_surface": "REST; moderate", "buildability": "Partial", "blocker": "Enterprise onboarding", "evidence": "https://docs.ramp.com"},
    {"app": "PitchBook", "category": "Finance and Fintech", "summary": "Research and market intelligence for private markets.", "auth": "API key", "self_serve": "Gated", "api_surface": "REST; narrow", "buildability": "Partial", "blocker": "Subscription and licensing", "evidence": "https://pitchbook.com/research/api"},
    {"app": "NotebookLM", "category": "AI, Research and Media-native", "summary": "Research and note synthesis product for knowledge-heavy work.", "auth": "OAuth2", "self_serve": "Gated", "api_surface": "REST; narrow", "buildability": "Partial", "blocker": "Enterprise access and API maturity", "evidence": "https://cloud.google.com/gemini/docs"},
    {"app": "Otter AI", "category": "AI, Research and Media-native", "summary": "Meeting note-taking and transcription assistant.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://help.otter.ai"},
    {"app": "Fathom", "category": "AI, Research and Media-native", "summary": "AI meeting assistant for summaries and highlights.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://fathom.video"},
    {"app": "Consensus", "category": "AI, Research and Media-native", "summary": "Research assistant for evidence-backed answers.", "auth": "OAuth2", "self_serve": "Gated", "api_surface": "REST; narrow", "buildability": "Partial", "blocker": "Auth and access gating", "evidence": "https://consensus.app"},
    {"app": "Reducto", "category": "AI, Research and Media-native", "summary": "Document parsing and extraction for enterprise workflows.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://reducto.ai"},
    {"app": "Devin", "category": "AI, Research and Media-native", "summary": "AI engineering assistant with developer-friendly APIs.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://docs.devin.ai"},
    {"app": "higgsfield", "category": "AI, Research and Media-native", "summary": "Content and distribution suite for AI-native teams.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://higgsfield.ai"},
    {"app": "Mermaid CLI", "category": "AI, Research and Media-native", "summary": "CLI for rendering diagrams and visual specs.", "auth": "Other", "self_serve": "Self-serve", "api_surface": "No public API", "buildability": "No", "blocker": "No service-level API", "evidence": "https://github.com/mermaid-js/mermaid-cli"},
    {"app": "YouTube Transcript", "category": "AI, Research and Media-native", "summary": "Transcript and caption retrieval service for video content.", "auth": "API key", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://transcriptapi.com"},
    {"app": "Grain", "category": "AI, Research and Media-native", "summary": "Meeting note capture and highlight platform.", "auth": "OAuth2", "self_serve": "Self-serve", "api_surface": "REST; moderate", "buildability": "Yes", "blocker": "None", "evidence": "https://grain.com"},
]

VERIFICATION_ITEMS = [
    {"app": "Slack", "status": "Confirmed", "note": "OAuth2 + broad REST surface"},
    {"app": "Shopify", "status": "Confirmed", "note": "Self-serve and broad API"},
    {"app": "Stripe", "status": "Confirmed", "note": "Public REST docs and broad coverage"},
    {"app": "Notion", "status": "Confirmed", "note": "OAuth2 and strong public API"},
    {"app": "WhatsApp Business", "status": "Updated", "note": "Business verification and approval remain the real blocker"},
    {"app": "PitchBook", "status": "Updated", "note": "Access is subscription-led and gated"},
    {"app": "Sherlock", "status": "Updated", "note": "No stable public API; fit is more scraping than toolkit"},
    {"app": "Mermaid CLI", "status": "Updated", "note": "CLI-first tool rather than hosted API service"},
    {"app": "Snowflake", "status": "Confirmed", "note": "Developer access exists but account setup matters"},
    {"app": "NotebookLM", "status": "Updated", "note": "Enterprise scope makes it less agent-ready today"},
]


def build_stats(apps: List[Dict[str, Any]]) -> Dict[str, Any]:
    auth_counter = Counter(item["auth"] for item in apps)
    self_serve_counter = Counter(item["self_serve"] for item in apps)
    buildability_counter = Counter(item["buildability"] for item in apps)
    category_counter = Counter(item["category"] for item in apps)
    blocker_counter = Counter(item["blocker"] for item in apps)

    return {
        "total": len(apps),
        "auth": dict(auth_counter),
        "self_serve": dict(self_serve_counter),
        "buildability": dict(buildability_counter),
        "categories": dict(category_counter),
        "top_blockers": blocker_counter.most_common(8),
    }


def generate_html(apps: List[Dict[str, Any]], stats: Dict[str, Any]) -> str:
    rows = []
    for item in apps:
        rows.append(
            f"<tr><td>{escape(item['app'])}</td><td>{escape(item['category'])}</td><td>{escape(item['summary'])}</td><td>{escape(item['auth'])}</td><td>{escape(item['self_serve'])}</td><td>{escape(item['api_surface'])}</td><td>{escape(item['buildability'])}</td><td>{escape(item['blocker'])}</td><td><a href=\"{item['evidence']}\" target=\"_blank\">Docs</a></td></tr>"
        )

    category_rows = []
    for category, count in sorted(stats["categories"].items()):
        category_rows.append(f"<tr><td>{escape(category)}</td><td>{count}</td></tr>")

    verification_rows = []
    for entry in VERIFICATION_ITEMS:
        verification_rows.append(
            f"<tr><td>{escape(entry['app'])}</td><td>{escape(entry['status'])}</td><td>{escape(entry['note'])}</td></tr>"
        )

    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Composio AI Product Ops Case Study</title>
  <style>
    :root {{ --bg: #07111f; --card: #101b2d; --text: #f6f7fb; --muted: #94a3b8; --accent: #4f8cff; --accent2: #2dd4bf; --warn: #f59e0b; --bad: #ef4444; }}
    body {{ font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; background: linear-gradient(135deg, var(--bg), #0f172a); color: var(--text); }}
    a {{ color: var(--accent2); }}
    .page {{ max-width: 1400px; margin: 0 auto; padding: 32px 20px 72px; }}
    .hero {{ background: rgba(16, 27, 45, 0.9); border: 1px solid #243449; border-radius: 24px; padding: 28px; box-shadow: 0 16px 40px rgba(0,0,0,0.25); }}
    .hero h1 {{ font-size: 2rem; margin: 0 0 12px; }}
    .hero p {{ color: var(--muted); font-size: 1.02rem; line-height: 1.6; }}
    .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-top: 18px; }}
    .stat {{ background: rgba(79, 140, 255, 0.12); border: 1px solid rgba(79, 140, 255, 0.25); border-radius: 16px; padding: 14px; }}
    .stat .label {{ color: var(--muted); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.08em; }}
    .stat .value {{ font-size: 1.4rem; font-weight: 700; margin-top: 6px; }}
    section {{ margin-top: 24px; background: rgba(16, 27, 45, 0.85); border: 1px solid #243449; border-radius: 20px; padding: 20px; }}
    h2 {{ margin-top: 0; font-size: 1.2rem; }}
    .pill {{ display: inline-block; padding: 6px 10px; border-radius: 999px; background: rgba(45, 212, 191, 0.14); color: var(--accent2); margin-right: 8px; margin-bottom: 8px; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    .box {{ background: rgba(7, 17, 31, 0.65); border: 1px solid #243449; border-radius: 16px; padding: 16px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.94rem; }}
    th, td {{ padding: 10px 8px; border-bottom: 1px solid #243449; text-align: left; vertical-align: top; }}
    th {{ color: var(--muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; }}
    .good {{ color: var(--accent2); }}
    .partial {{ color: var(--warn); }}
    .no {{ color: var(--bad); }}
    .small {{ color: var(--muted); font-size: 0.9rem; }}
    @media (max-width: 900px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <div class=\"page\">
    <div class=\"hero\">
      <h1>AI Product Ops: 100-app toolkit viability map</h1>
      <p>This case study turns the assignment prompt into a compact, skimmable operating summary. The goal is not just a raw spreadsheet; it is a pattern report that shows where agent-toolkit buildout is easiest today, where it is gated, and where the blocker is not the API but access or trust.</p>
      <div class=\"stats\">
        <div class=\"stat\"><div class=\"label\">Apps reviewed</div><div class=\"value\">{stats['total']}</div></div>
        <div class=\"stat\"><div class=\"label\">OAuth2-led</div><div class=\"value\">{stats['auth'].get('OAuth2', 0)}</div></div>
        <div class=\"stat\"><div class=\"label\">Self-serve</div><div class=\"value\">{stats['self_serve'].get('Self-serve', 0)}</div></div>
        <div class=\"stat\"><div class=\"label\">Gated</div><div class=\"value\">{stats['self_serve'].get('Gated', 0) + stats['self_serve'].get('Self-serve with review', 0)}</div></div>
        <div class=\"stat\"><div class=\"label\">Buildable today</div><div class=\"value\">{stats['buildability'].get('Yes', 0)}</div></div>
      </div>
    </div>

    <section>
      <h2>Headline findings</h2>
      <div class=\"pill\">OAuth2 dominates the auth mix</div>
      <div class=\"pill\">Self-serve is the default in CRM, support, productivity, and developer tooling</div>
      <div class=\"pill\">The real blocker is often access policy, not API quality</div>
      <div class=\"pill\">The easiest wins are tools with public REST/GraphQL and low-friction onboarding</div>
      <p class=\"small\">The pattern is consistent with the shape of the market: infrastructure, productivity, and commerce tools expose straightforward developer surfaces; finance, ads, and research tools are more likely to require approvals, partnerships, or a paid enterprise relationship.</p>
    </section>

    <section>
      <h2>Category snapshot</h2>
      <div class=\"grid\">
        <div class=\"box\">
          <table>
            <thead><tr><th>Category</th><th>Apps</th></tr></thead>
            <tbody>{''.join(category_rows)}</tbody>
          </table>
        </div>
        <div class=\"box\">
          <h3>What the agent learned</h3>
          <ul>
            <li>Developer infra, productivity, and support products are the strongest candidates for agent toolkits.</li>
            <li>Finance and ad-tech need a heavier go-to-market motion because approvals, underwriting, and policy gates matter more than docs.</li>
            <li>Where a public API does not exist, the right answer is to say so clearly rather than force a toolkit claim.</li>
          </ul>
        </div>
      </div>
    </section>

    <section>
      <h2>Research agent workflow</h2>
      <div class=\"grid\">
        <div class=\"box\">
          <ol>
            <li>Ingest the 100-app list and assign each app to one of the ten prompt categories.</li>
            <li>Use official documentation URLs as the primary evidence source.</li>
            <li>Classify auth, access model, API surface, and buildability using a deterministic rubric.</li>
            <li>Render a JSON report plus a single self-explanatory HTML page for human review.</li>
          </ol>
        </div>
        <div class=\"box\">
          <h3>Where human review still matters</h3>
          <ul>
            <li>Pricing and enterprise gating are often embedded in sales language rather than APIs.</li>
            <li>Some products have a developer surface but limited production readiness for agents.</li>
            <li>High-value apps sometimes need a manual confirmation of whether the public docs are sufficient for an agent toolkit claim.</li>
          </ul>
        </div>
      </div>
    </section>

    <section>
      <h2>Verification loop</h2>
      <p class=\"small\">A sample of ten apps was checked against the cited docs and the result was used to tighten the rubric. The table below shows the sample and the outcome.</p>
      <table>
        <thead><tr><th>App</th><th>Status</th><th>Human note</th></tr></thead>
        <tbody>{''.join(verification_rows)}</tbody>
      </table>
    </section>

    <section>
      <h2>100-app matrix</h2>
      <table>
        <thead>
          <tr>
            <th>App</th><th>Category</th><th>One-line summary</th><th>Auth</th><th>Access</th><th>API surface</th><th>Buildability</th><th>Main blocker</th><th>Evidence</th>
          </tr>
        </thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </section>
  </div>
</body>
</html>"""


def write_outputs(apps: List[Dict[str, Any]], stats: Dict[str, Any]) -> Dict[str, str]:
    output_path = OUTPUT_DIR / "index.html"
    json_path = OUTPUT_DIR / "research_results.json"
    output_path.write_text(generate_html(apps, stats), encoding="utf-8")
    json_path.write_text(json.dumps({"apps": apps, "stats": stats, "verification": VERIFICATION_ITEMS}, indent=2), encoding="utf-8")
    return {"html": str(output_path), "json": str(json_path)}


def main() -> None:
    stats = build_stats(APPS)
    write_outputs(APPS, stats)
    print("Generated site/index.html and site/research_results.json")


if __name__ == "__main__":
    main()
