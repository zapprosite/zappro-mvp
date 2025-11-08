# 📝 MARKDOWN AUDIT & REFINEMENT TASK

**Data:** 7 Nov 2025  
**Owner:** Codex CLI (GPT-5)  
**Priority:** High  
**Timeline:** 45 minutes

---

## Objective

Audit ALL .md files in ZapPro repository and improve:
1. **Clarity & Readability** — Clear headings, logical flow, scannable content
2. **Consistency** — Same formatting across all docs (headings, lists, code blocks)
3. **Professional Standards** — 2025 GitHub + IBM + Ed-Fi best practices
4. **Completeness** — TOC for long docs, working links, real examples
5. **SEO & Discoverability** — Better structure, keywords, internal linking

---

## Files to Audit & Improve

### Priority 1 (Main docs)
- [ ] README.md
- [ ] docs/AGENTS.md
- [ ] docs/SECURITY.md
- [ ] docs/WORKFLOW.md
- [ ] docs/DECISION.md
- [ ] PRD.md

### Priority 2 (Tutor docs)
- [ ] tutor/prompt.md
- [ ] tutor/progress.state.md (if exists)

### Priority 3 (Additional)
- [ ] docs/LOG.md (if exists)
- [ ] docs/how-to-run.md (if exists)

---

## Markdown Best Practices 2025 (Apply to All)

### Heading Structure
✅ **DO:**
- Single H1 as main title only (no stacking H1s)
- Logical hierarchy: H1 → H2 → H3 (no skipping levels)
- Blank lines above/below headings
- Concise, action-oriented titles: "## How to Deploy" NOT "## Deployment Information"

❌ **DON'T:**
- Multiple H1s per file
- H2 directly followed by H4
- Decorative characters in headings
- Vague headings

### Lists & Formatting
✅ **DO:**
- Unordered lists: use `-` consistently
- Ordered lists only for sequential steps
- Bold for emphasis: `**important**` NOT `__important__`
- Inline code: backticks for commands/file paths
- Code blocks: ALWAYS specify language (bash, python, yaml, json, sql, html, typescript)

Example:
make test

text

NOT:
make test

text

### Tables
✅ **DO:**
- Use for structured data (2+ columns, 3+ rows)
- Readable cell content (<60 chars per cell)
- Left-align text, right-align numbers
- Clear column headers

❌ **DON'T:**
- Use tables for prose paragraphs
- Nested tables
- Overly complex multi-column tables

### GitHub Alerts (NEW: 2025)
Use these for important information:

[!NOTE]
This is general information

[!TIP]
This is helpful advice

[!IMPORTANT]
Critical information

[!WARNING]
Warning or caution

[!CAUTION]
Danger - be careful

text

### Links & Navigation
✅ **DO:**
- Use descriptive link text: `[docs/AGENTS.md](./docs/AGENTS.md)` NOT `[here](link)`
- Relative paths for internal links: `./docs/file.md`
- TOC with working links for docs >500 words
- Verify all links work (no broken references)

❌ **DON'T:**
- Absolute URLs for internal docs
- Generic link text like "here", "click", "link"
- Dead links or outdated paths

### Code & Examples
✅ **DO:**
- Complete, runnable examples
- Real file paths, real command output
- Include error handling + expected output
- No placeholders (YOURTOKEN, TODO, etc.)

❌ **DON'T:**
- Pseudo-code or pseudo-examples
- Placeholders like [FILL HERE]
- Incomplete commands
- Copy-paste errors

---

## Specific File Improvements

### README.md
- [ ] Add Table of Contents after intro (for navigation)
- [ ] Organize sections: Problem → Solution → Tech Stack → Quick Start → Commands → Docs Links
- [ ] Move badges to top
- [ ] All code blocks: specify language (bash, python)
- [ ] Verify all links work (relative paths)
- [ ] Add "Getting Help" section at bottom
- [ ] Fix any broken internal links (e.g., [docs/AGENTS.md](./docs/AGENTS.md))

### docs/AGENTS.md
- [ ] Add Table of Contents (file >2000 words)
- [ ] Fix heading hierarchy (check for skipped levels)
- [ ] Replace description tables with proper formatting
- [ ] Add GitHub alerts for critical rules (NOTE for must-haves, WARNING for don'ts)
- [ ] All code blocks: language tags (yaml, python, bash)
- [ ] Consistent bold/emphasis formatting
- [ ] Real examples, no placeholders

### docs/SECURITY.md
- [ ] Add "Quick Reference" GitHub alert box at top
- [ ] Organize sections by severity: CRITICAL → HIGH → MEDIUM → LOW
- [ ] Use proper tables for vulnerability response times
- [ ] Add checklist boxes ✓ for compliance items
- [ ] Clear link to security contact + escalation path
- [ ] GitHub alerts for important warnings

### docs/WORKFLOW.md
- [ ] Add "At a Glance" diagram section (ASCII or description)
- [ ] Check heading hierarchy (no H4 without H3 parent)
- [ ] Number steps for PR process (1. 2. 3.)
- [ ] Replace prose explanations with clear bullet points + examples
- [ ] Add "Troubleshooting" section before FAQ
- [ ] Code blocks: language tags (bash, git commands)

### docs/DECISION.md
- [ ] Simplify criteria explanation (currently dense)
- [ ] Add decision tree diagram or flow (ASCII or description)
- [ ] Move implementation roadmap higher up
- [ ] Better descriptions for each module decision
- [ ] Organize by Module Type (Backend → Frontend → DevOps)
- [ ] Add risk/effort matrix as visual table

### PRD.md
- [ ] Add Executive Summary box (GitHub alert NOTE or highlighted)
- [ ] Fix table formatting (columns are too wide)
- [ ] Better section organization: MVP Scope → Tech Stack → Features → Timeline
- [ ] Organize features: MVP Phase 1 → Phase 2 → Phase 3+
- [ ] Add data model relationships (ASCII diagram or table)
- [ ] Success criteria as numbered checklist
- [ ] Clear roadmap with timeline

### tutor/prompt.md
- [ ] Add "Quick Start" section at very top
- [ ] Better rule numbering (clearly label 1-7 Golden Rules)
- [ ] Add context reading checklist
- [ ] Replace long paragraphs with bullet points
- [ ] Add escalation decision tree (ASCII or description)
- [ ] Consistent formatting throughout

---

## Validation Steps (REQUIRED Before Commit)

1. **Markdown Lint Check**
find . -name "*.md" -type f | head -10

Verify each file exists
text

2. **Link Validation (Manual)**
- Open each .md in GitHub preview
- Click each internal link
- Verify no broken references

3. **Visual Rendering**
- Render each .md locally in VS Code
- Verify headings render correctly
- Check table alignment
- Confirm code blocks highlight with language syntax

4. **Content Accuracy**
- Verify all file paths referenced actually exist
- Verify all commands are executable
- Ensure examples produce expected output
- Check no stale/outdated information

---

## Expected Commit Output

### Files Modified (in single atomic commit)
- README.md
- docs/AGENTS.md
- docs/SECURITY.md
- docs/WORKFLOW.md
- docs/DECISION.md
- PRD.md
- tutor/prompt.md
- (+ any other .md files found)

### Commit Message Template
docs: refactor all .md files per 2025 best practices

Add/verify heading hierarchy (no skipping H2→H4)

Reorganize docs: structure → TOC → content

Use GitHub alerts (NOTE, WARNING, IMPORTANT, TIP)

Verify all code blocks have language tags (bash, python, yaml)

Fix relative link paths (./docs/file.md format)

Add Table of Contents for files >500 words

Consistent list formatting (- for bullets, 1. for ordered)

Professional tone + real examples (no placeholders)

Improved readability: clear sections, scannable format

All docs now follow 2025 GitHub markdown standards

Validation passed:
✓ All headings render correctly
✓ All internal links work
✓ All code blocks highlight
✓ No broken references

text

---

## MCP Tools to Use

| Task | MCP Tool |
|------|----------|
| Read .md files | filesystem |
| Write improved .md | filesystem |
| Find all .md files | shell (\`find . -name "*.md"\`) |
| Commit changes | git |
| Verify links | (manual check in GitHub preview) |

---

## Success Criteria

✅ All .md files follow 2025 GitHub markdown standards  
✅ Headings organized logically (H1 → H2 → H3)  
✅ All code blocks have language tags  
✅ GitHub alerts used for NOTE/WARNING/TIP  
✅ TOC added for docs >500 words  
✅ All internal links verified as working  
✅ Professional, scannable content  
✅ One atomic commit with all improvements  

---

## Timeline
- **Estimated:** 45 minutes
- **Complexity:** Medium (systematic audit + improvements)
- **Risk:** Low (no code changes, just documentation)

---

**Ready for Codex CLI execution.**
