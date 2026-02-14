---
created: 2026-02-13T14:41:49Z
last_updated: 2026-02-13T14:41:49Z
version: 1.0
author: Claude Code PM System
---

# Project Brief

## What It Does

The **ASO (App Store Optimization) Agent System** is a production-ready multi-agent framework for Claude Code that automates app store optimization for iOS and Android apps. It combines specialized AI agents with real-time data fetching to generate actionable, copy-paste ready deliverables.

## Why It Exists

App Store Optimization is critical for mobile app discoverability but traditionally requires expensive tools (AppTweak, Sensor Tower) or manual, time-consuming analysis. This project provides a free, AI-powered alternative that delivers professional-grade ASO outputs using only free data sources (iTunes Search API).

## Core Value Proposition

- **Free** - No paid API subscriptions required
- **Actionable** - Generates copy-paste ready metadata, not just reports
- **Automated** - Multi-agent workflow handles research, optimization, and strategy
- **Dual Platform** - Covers both Apple App Store and Google Play Store
- **Character-Validated** - All metadata respects platform character limits

## Target Users

1. **Indie App Developers** - Solo developers launching apps who need ASO guidance
2. **App Marketers** - Marketing professionals managing app store presence
3. **ASO Specialists** - Professionals seeking to accelerate their workflow
4. **Development Teams** - Teams integrating ASO into their CI/CD pipeline

## Success Criteria

- Generate character-validated metadata for both Apple and Google platforms
- Provide actionable task checklists with specific dates (not placeholders)
- Fetch real competitor data via iTunes Search API
- Complete full audit workflow in 30-40 minutes
- Produce 5-phase structured output with copy-paste ready content

## Scope

### In Scope
- Keyword research and prioritization
- Metadata optimization (titles, descriptions, keywords)
- Competitor analysis and gap identification
- Pre-launch checklists (47 items)
- A/B test planning
- Review response templates
- Launch timeline generation

### Out of Scope
- Paid acquisition (Apple Search Ads, Google Ads)
- App analytics integration
- Real-time ranking tracking
- Automated app store submissions
- Screenshot/video asset creation (provides specs only)

## Key Constraints

- **Zero External Dependencies** - Python standard library only
- **Free Data Sources Only** - iTunes Search API, no paid APIs
- **Platform Compliance** - Apple (30/30/170/100/4000) and Google (50/80/4000) character limits
- **Python 3.8+** - Backward compatibility requirement
