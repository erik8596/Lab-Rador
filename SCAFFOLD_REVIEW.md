# Scaffold Review: Reality Check

## ✅ SOLID Design Decisions

1. **Modular Architecture** — agents, generators, api separate ✓
2. **Pydantic Models** — Type safety and validation ✓
3. **Typer CLI** — Simple, modern, sufficient ✓
4. **Prompt Templates** — Manageable as .md files ✓
5. **Test Structure** — Good foundation ✓
6. **Config Module** — Environment management ✓

---

## ⚠️ UNREALISTIC / SCOPE CREEP

### 1. **Unnecessary Dependencies**
- `numpy`, `pandas`, `scikit-learn`, `joblib`, `scipy` - **NOT NEEDED**
  - These were in original requirements but not used
  - **Action**: Remove these, they bloat the project
  
- `click` - **REDUNDANT**
  - Typer uses click internally
  - **Action**: Remove explicit click dependency

### 2. **Over-Engineering: Protocol Analyzer Agent**
- `agents/protocol_analyzer.py` — Safety checks + equipment compatibility
- **Reality**: For MVP, this is premature
- **Action**: Remove for now, focus on generator + refiner first
- **Can add**: In Phase 2 if time permits

### 3. **Over-Engineering: protocols.io Client**
- `api/protocols_io_client.py` — Full API integration
- **Reality**: protocols.io has complex auth, querying, and rate limits
- **For hackathon MVP**: NOT worth the complexity
- **Action**: Remove for now, or leave as stub comment
- **Can add**: If we need to import existing protocols

### 4. **Opentrons Generator Realism**
- Current scope: "Generate executable Opentrons scripts"
- **Reality Check**: 
  - Opentrons API is COMPLEX (deck setup, labware, pipettes, tips, etc.)
  - We can't generate fully functional scripts without deep domain knowledge
  - **Better approach**: Generate skeleton/template with comments, not working code
- **Action**: Rename to "template generator" - shows structure but needs human refinement

### 5. **Empty Data Catalogs**
- `data/equipment_catalog.json` — Empty
- `data/materials_catalog.json` — Empty
- **Problem**: Validation logic depends on these
- **Action**: Either:
  a) Populate with real lab equipment/materials (time-intensive)
  b) Mark as optional/future enhancement
  c) Use simple lists instead of complex catalogs

### 6. **Generator Templates**
- `generators/templates/opentrons_base.py` — Empty template
- `generators/templates/markdown_base.md` — Empty template
- **Issue**: Do we actually need templates or should we generate inline?
- **Action**: Decide: template system or simpler inline generation?

---

## 🎯 WHAT'S MISSING (Critical)

### 1. **Configuration Loading**
- `config/settings.py` is stub
- **Needed**: Actually load .env file, validate ANTHROPIC_API_KEY
- **Action**: Implement before Phase 1

### 2. **Error Handling Strategy**
- `core/exceptions.py` lists TODO exceptions
- **Needed**: Define actual exception hierarchy
- **Action**: Define before Phase 1

### 3. **Protocol Schema Definition**
- `docs/PROTOCOL_SCHEMA.md` is empty
- **Needed**: JSON schema for protocol structure (BEFORE generators)
- **Action**: Define schema before Phase 2 (generators)

### 4. **Claude Prompt Strategy**
- `agents/prompts/protocol_generation.md` is empty
- **Needed**: Well-crafted prompt with examples
- **Critical**: This makes or breaks the whole system
- **Action**: Research + write before Phase 1 (agents)

### 5. **Test Mocking Strategy**
- No mock for Anthropic API
- `tests/conftest.py` is empty
- **Needed**: Mock Claude responses for testing
- **Action**: Set up before Phase 5 (tests)

---

## 📊 Realistic Implementation Priority

### MUST DO (Hackathon Core)
1. **Config + Environment** — Load .env, validate keys
2. **Core Models** — Define Protocol, Step, Material, Equipment
3. **Claude API Wrapper** — Call Claude, parse responses
4. **Protocol Generator** — NL → Protocol via Claude
5. **Markdown Generator** — Pretty output
6. **CLI Generator Command** — `lab-rador generate "..."`
7. **Basic Tests** — Unit tests with mocking

### SHOULD DO (MVP Enhancement)
8. **CLI Refine Command** — Iterative improvement
9. **Opentrons Template Generator** — Skeleton scripts
10. **Export Command** — Multiple formats
11. **List Command** — Show protocols

### NICE TO HAVE (Phase 2)
12. **Protocol Analyzer** — Safety checks
13. **Data Validation** — Equipment/material catalogs
14. **protocols.io Integration** — Pull real protocols
15. **Advanced Testing** — Integration tests

---

## 💡 Recommended Scaffold Adjustments

### REMOVE (Scope Creep)
- [ ] `api/protocols_io_client.py` → Keep as comment/future
- [ ] `agents/protocol_analyzer.py` → Remove for now
- [ ] Unnecessary dependencies (numpy, pandas, scipy, scikit-learn, joblib, click)
- [ ] Empty data catalogs (or keep as placeholders with comments)

### KEEP (Core Path)
- [x] Config module
- [x] Core models  
- [x] Agents (generator + refiner)
- [x] Generators (markdown + json)
- [x] Opentrons (as template generator, not executable)
- [x] CLI structure
- [x] Tests
- [x] Utils (validators, logging, formatters)

### ADD/CLARIFY
- [ ] Define exception hierarchy in `core/exceptions.py`
- [ ] Define protocol JSON schema (for validation + generation)
- [ ] Write Claude prompt template (CRITICAL)
- [ ] Mock strategy for tests
- [ ] Realistic Opentrons output expectations

---

## 🏆 Realistic Hackathon Scope

**Core Feature (Doable in Hackathon)**:
```
Natural Language Description 
    ↓
Claude API (with good prompt)
    ↓
Structured Protocol JSON
    ↓
Multiple Outputs (Markdown, JSON, Opentrons Skeleton)
    ↓
Iterative Refinement Loop
```

**MVP User Journey**:
1. User: `lab-rador generate "Mix 100mL A with 50mL B, heat to 60C for 15 min"`
2. System: Calls Claude with protocol schema instructions
3. Claude: Returns structured protocol JSON
4. System: Generates Markdown (human-readable) + Opentrons skeleton
5. User: `lab-rador refine protocol.json "Add more safety notes"`
6. System: Iterates with Claude using feedback

**NOT MVP** (Can't do in hackathon):
- Full Opentrons executable scripts (too domain-complex)
- Real protocols.io integration (API auth complexity)
- Equipment/material validation (data doesn't exist)
- Safety analysis agent (complex reasoning needed)

---

## ✋ DECISION POINT

Should we:

**Option A: Clean Up Now** (Recommended)
- Remove scope creep items
- Trim dead dependencies
- Document realistic outputs
- Commit "v2 - Realistic Scope"

**Option B: Keep Full Structure**
- Mark unrealistic items as "FUTURE"
- Proceed with implementation
- Scope-limit each phase as needed

**I recommend Option A** — Leaner codebase, clearer goals, easier to execute.

