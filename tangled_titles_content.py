"""Structured content for the Interview and Power Map pages.

The app renders both pages from these objects so interview themes and power-map
nodes stay aligned as the synthesis evolves.
"""

from __future__ import annotations


LEVELS = {
    "Central Issue": {"color": "#4f8f5b", "group": "Central"},
    "Individual Level Factors": {"color": "#6fa8c8", "group": "Individual"},
    "Interpersonal Level Factors": {"color": "#d7839a", "group": "Interpersonal"},
    "Community Level Factors": {"color": "#efb05d", "group": "Community"},
    "Structural Factors": {"color": "#b9d98b", "group": "Structural"},
    "Policy-Level Determinants": {"color": "#d7e8bd", "group": "Structural"},
    "Economic-Level Determinants": {"color": "#d7e8bd", "group": "Structural"},
    "Societal Determinants": {"color": "#d7e8bd", "group": "Structural"},
}

STRUCTURAL_SUBLEVELS = (
    "Policy-Level Determinants",
    "Economic-Level Determinants",
    "Societal Determinants",
)

LEVEL_ORDER = (
    "Central Issue",
    "Individual Level Factors",
    "Interpersonal Level Factors",
    "Community Level Factors",
    "Structural Factors",
    "Policy-Level Determinants",
    "Economic-Level Determinants",
    "Societal Determinants",
)

THEME_LEVEL_ORDER = (
    "Central Issue",
    "Individual",
    "Interpersonal",
    "Community",
    "Structural",
    "Economic",
    "Societal",
    "Policy",
)


POWER_NODES = [
    {
        "id": "tangled_titles",
        "label": "Tangled Titles",
        "level": "Central Issue",
        "type": "Mixed",
        "description": "A legal and social condition where the person living in or caring for a property cannot fully exercise ownership rights because the deed, inheritance, probate status, or title record does not align with lived family arrangements.",
        "related_interview_themes": ["title_blocks_equity", "crisis_visibility", "housing_stability"],
    },
    {
        "id": "lack_of_knowledge",
        "label": "Lack of knowledge about home transfers and heirs' property",
        "level": "Individual Level Factors",
        "type": "Barrier",
        "description": "Residents often do not know that they need probate, deed transfer, estate administration, or formal title clearing after a homeowner dies.",
        "related_interview_themes": ["knowledge_gap", "inheritance_myth", "register_of_wills_gap"],
    },
    {
        "id": "not_engaged_estate_planning",
        "label": "Not engaged in estate planning",
        "level": "Individual Level Factors",
        "type": "Barrier",
        "description": "Homeowners may discuss wishes informally but do not complete wills, transfer-on-death deeds, life estate deeds, probate, or recorded deed transfers.",
        "related_interview_themes": ["estate_planning_avoidance", "death_and_asset_taboo", "preventive_planning"],
    },
    {
        "id": "costly_process",
        "label": "Costly legal and administrative process",
        "level": "Individual Level Factors",
        "type": "Barrier",
        "description": "Probate, title clearing, distant heir outreach, legal consultation, and deed recording can create costs that prevent residents from starting or completing the process.",
        "related_interview_themes": ["legal_cost_barrier", "administrative_burden"],
    },
    {
        "id": "engagement_estate_planning",
        "label": "Engagement with estate planning",
        "level": "Individual Level Factors",
        "type": "Facilitator",
        "description": "Wills, transfer-on-death deeds, life estate deeds, and other preventive tools can reduce future tangled title problems.",
        "related_interview_themes": ["preventive_planning", "transfer_on_death_deed"],
    },
    {
        "id": "digital_and_document_burden",
        "label": "Digital and document burden",
        "level": "Individual Level Factors",
        "type": "Barrier",
        "description": "Older homeowners may struggle with email, websites, online forms, uploaded documents, IDs, SSNs, utility bills, mortgage records, and deed paperwork.",
        "related_interview_themes": ["digital_divide", "document_collection_burden"],
    },
    {
        "id": "family_disagreement",
        "label": "Familial disagreements over home ownership",
        "level": "Interpersonal Level Factors",
        "type": "Barrier",
        "description": "Siblings, heirs, or extended family members may disagree about who owns, lives in, repairs, sells, or inherits the property.",
        "related_interview_themes": ["family_conflict", "joint_decision_burden", "contested_title"],
    },
    {
        "id": "no_clear_heir",
        "label": "No clear heir or unclear ownership pathway",
        "level": "Interpersonal Level Factors",
        "type": "Barrier",
        "description": "When no one agrees who should receive the property, or when several heirs have fractional claims, the home may remain legally unresolved.",
        "related_interview_themes": ["contested_title", "property_in_limbo"],
    },
    {
        "id": "partition_and_forced_sale",
        "label": "Partition and forced sale risk",
        "level": "Interpersonal Level Factors",
        "type": "Barrier",
        "description": "Fractional ownership can create vulnerability if one heir or outside buyer pushes for sale or division of the property.",
        "related_interview_themes": ["forced_sale_risk", "speculation_risk"],
    },
    {
        "id": "vulnerability_to_speculators",
        "label": "Vulnerability to speculators",
        "level": "Interpersonal Level Factors",
        "type": "Barrier",
        "description": "Speculators or investors may exploit unclear ownership, buy partial interests, or pressure families into sale.",
        "related_interview_themes": ["speculation_risk", "racialized_wealth_loss"],
    },
    {
        "id": "family_cohesion",
        "label": "Familial cohesion and collective decision-making",
        "level": "Interpersonal Level Factors",
        "type": "Facilitator",
        "description": "Families who can agree, sign over interests, or support the person living in the home can resolve title problems more easily.",
        "related_interview_themes": ["family_cohesion", "mediation"],
    },
    {
        "id": "mediation_services",
        "label": "Mediation services",
        "level": "Interpersonal Level Factors",
        "type": "Facilitator",
        "description": "Third-party mediation can help family members reach agreement when title issues are tied to conflict among heirs.",
        "related_interview_themes": ["mediation", "contested_title"],
    },
    {
        "id": "neighborhood_associations",
        "label": "Neighborhood associations",
        "level": "Community Level Factors",
        "type": "Facilitator",
        "description": "Local associations can identify residents at risk, host outreach, and connect households to trusted resources.",
        "related_interview_themes": ["community_outreach", "trusted_messengers"],
    },
    {
        "id": "block_captains",
        "label": "Block captains and community leaders",
        "level": "Community Level Factors",
        "type": "Facilitator",
        "description": "Trusted local leaders can do door-to-door outreach and help identify residents who may not seek formal legal help on their own.",
        "related_interview_themes": ["door_to_door_outreach", "trusted_messengers"],
    },
    {
        "id": "housing_service_organizations",
        "label": "Housing service organizations",
        "level": "Community Level Factors",
        "type": "Mixed",
        "description": "Home repair programs, housing counselors, and stabilization programs often encounter tangled titles when residents apply for assistance.",
        "related_interview_themes": ["home_repair_gateway", "service_eligibility_barrier"],
    },
    {
        "id": "legal_service_organizations",
        "label": "Legal service organizations",
        "level": "Community Level Factors",
        "type": "Facilitator",
        "description": "Legal aid groups help residents navigate probate, deed transfer, estate planning, tax sale prevention, and title clearing.",
        "related_interview_themes": ["legal_aid_facilitator", "holistic_legal_services"],
    },
    {
        "id": "mvls",
        "label": "Maryland Volunteer Legal Services",
        "level": "Community Level Factors",
        "type": "Facilitator",
        "description": "A key legal service provider offering support for probate, estate planning, title clearing, tax credits, and related legal issues.",
        "related_interview_themes": ["legal_aid_facilitator", "holistic_legal_services"],
    },
    {
        "id": "pro_bono_resource_center",
        "label": "Pro Bono Resource Center",
        "level": "Community Level Factors",
        "type": "Facilitator",
        "description": "A legal support organization that can connect residents with volunteer legal assistance.",
        "related_interview_themes": ["legal_aid_facilitator"],
    },
    {
        "id": "stop_oppressive_seizures_fund",
        "label": "Stop Oppressive Seizures Fund",
        "level": "Community Level Factors",
        "type": "Facilitator",
        "description": "A community and legal resource connected to housing stabilization, tax sale prevention, home repair, and property tax payment support.",
        "related_interview_themes": ["tax_sale_prevention", "housing_stabilization"],
    },
    {
        "id": "baltimore_neighborhood_indicators_alliance",
        "label": "Baltimore Neighborhood Indicators Alliance",
        "level": "Community Level Factors",
        "type": "Facilitator",
        "description": "A data partner that can support neighborhood-level identification of risk and spatial targeting of outreach.",
        "related_interview_themes": ["data_driven_outreach", "black_butterfly_geography"],
    },
    {
        "id": "referral_network",
        "label": "Referral network and warm handoffs",
        "level": "Community Level Factors",
        "type": "Mixed",
        "description": "Organizations can refer residents to legal aid, but warm handoffs and tracking are needed so residents actually return to the original service pipeline.",
        "related_interview_themes": ["referral_gap", "warm_handoff"],
    },
    {
        "id": "probate_process",
        "label": "Probate and estate administration",
        "level": "Policy-Level Determinants",
        "type": "Barrier",
        "description": "Probate is often required to move property out of the name of a deceased owner and into the name of a living heir.",
        "related_interview_themes": ["probate_barrier", "register_of_wills_gap"],
    },
    {
        "id": "register_of_wills",
        "label": "Register of Wills",
        "level": "Policy-Level Determinants",
        "type": "Mixed",
        "description": "A formal administrative point for opening an estate and initiating probate, but many residents do not know this office is relevant.",
        "related_interview_themes": ["register_of_wills_gap", "administrative_burden"],
    },
    {
        "id": "legal_paperwork_to_titled_owner",
        "label": "Legal paperwork addressed to the titled owner",
        "level": "Policy-Level Determinants",
        "type": "Barrier",
        "description": "Notices, lawsuits, foreclosure documents, and tax sale paperwork may be sent to the deceased or titled owner rather than the person actually living in the home.",
        "related_interview_themes": ["formal_system_mismatch", "tax_sale_vulnerability"],
    },
    {
        "id": "owner_occupied_protection_gap",
        "label": "Loss of owner-occupied protections",
        "level": "Policy-Level Determinants",
        "type": "Barrier",
        "description": "Residents with tangled titles may not receive the legal protections, tax credits, or program eligibility associated with owner-occupied property.",
        "related_interview_themes": ["owner_occupied_protection_gap", "service_eligibility_barrier"],
    },
    {
        "id": "tax_sale_system",
        "label": "Tax sale and foreclosure system",
        "level": "Policy-Level Determinants",
        "type": "Barrier",
        "description": "Unpaid property taxes, water bills, or municipal charges can move a property toward tax sale, foreclosure, and eventual loss.",
        "related_interview_themes": ["tax_sale_vulnerability", "housing_loss"],
    },
    {
        "id": "heirs_property_rights",
        "label": "Heirs' property rights",
        "level": "Policy-Level Determinants",
        "type": "Mixed",
        "description": "Legal protections for heirs' property can influence whether families can challenge forced sales, retain homes, or resolve fractional ownership.",
        "related_interview_themes": ["forced_sale_risk", "policy_reform"],
    },
    {
        "id": "maryland_intestacy_law",
        "label": "Maryland intestacy law",
        "level": "Policy-Level Determinants",
        "type": "Barrier",
        "description": "When there is no will, state law determines inheritance and may not match the family's informal expectations or nontraditional family structure.",
        "related_interview_themes": ["inheritance_myth", "contested_title"],
    },
    {
        "id": "transfer_on_death_deed",
        "label": "Transfer-on-death deed",
        "level": "Policy-Level Determinants",
        "type": "Facilitator",
        "description": "A preventive deed tool that can make post-death property transfer simpler and less expensive.",
        "related_interview_themes": ["transfer_on_death_deed", "preventive_planning"],
    },
    {
        "id": "repair_grant_estate_planning_link",
        "label": "Link repair grants with estate planning",
        "level": "Policy-Level Determinants",
        "type": "Facilitator",
        "description": "Home repair assistance could be paired with estate planning, title clearing, or mediation while homeowners are still alive.",
        "related_interview_themes": ["repair_grant_policy", "preventive_planning"],
    },
    {
        "id": "eminent_domain_asset_forfeiture",
        "label": "Eminent domain and civil asset forfeiture",
        "level": "Policy-Level Determinants",
        "type": "Barrier",
        "description": "Public taking, forfeiture, and related legal powers can compound property insecurity when residents already lack clear title or recognized ownership standing.",
        "related_interview_themes": ["tax_sale_vulnerability", "black_butterfly_geography"],
    },
    {
        "id": "reparations_commission_remediation",
        "label": "Reparations-oriented tangled-title remediation",
        "level": "Policy-Level Determinants",
        "type": "Facilitator",
        "description": "Policy proposals can prioritize tangled-title remediation as part of broader repair for racialized housing and wealth extraction.",
        "related_interview_themes": ["black_butterfly_geography", "title_blocks_equity"],
    },
    {
        "id": "high_cost_title_clearing",
        "label": "High cost of title-clearing and estate-planning services",
        "level": "Economic-Level Determinants",
        "type": "Barrier",
        "description": "Legal and title services can be unaffordable for residents on fixed or low incomes.",
        "related_interview_themes": ["legal_cost_barrier", "fixed_income_seniors"],
    },
    {
        "id": "fixed_income_seniors",
        "label": "Fixed-income older homeowners",
        "level": "Economic-Level Determinants",
        "type": "Barrier",
        "description": "Seniors on pensions, SSI, retirement income, or limited earnings may be unable to afford major repairs, legal help, taxes, or administrative costs.",
        "related_interview_themes": ["fixed_income_seniors", "repair_cost_burden"],
    },
    {
        "id": "rising_repair_costs",
        "label": "Rising repair costs",
        "level": "Economic-Level Determinants",
        "type": "Barrier",
        "description": "Contractor costs, materials, and maintenance costs have risen while many older homeowners' incomes remain fixed.",
        "related_interview_themes": ["repair_cost_burden", "deferred_maintenance"],
    },
    {
        "id": "annual_tax_lien_sales",
        "label": "Annual tax lien sales",
        "level": "Economic-Level Determinants",
        "type": "Barrier",
        "description": "Tax lien sales can turn unpaid taxes, bills, and municipal charges into foreclosure risk and loss of homeownership.",
        "related_interview_themes": ["tax_sale_vulnerability", "housing_loss"],
    },
    {
        "id": "housing_affordability_tradeoff",
        "label": "Housing affordability trade-off",
        "level": "Economic-Level Determinants",
        "type": "Barrier",
        "description": "A paid-off family home may be far cheaper than market rent, so losing it can create immediate displacement risk.",
        "related_interview_themes": ["shelter_security", "housing_loss"],
    },
    {
        "id": "information_gap",
        "label": "Information gap",
        "level": "Societal Determinants",
        "type": "Barrier",
        "description": "Residents often lack accessible public information about what happens to a house after death, what probate is, or why title matters.",
        "related_interview_themes": ["information_gap", "inheritance_myth"],
    },
    {
        "id": "historic_modern_segregation",
        "label": "Historic and modern segregation",
        "level": "Societal Determinants",
        "type": "Barrier",
        "description": "Historic redlining and contemporary segregation shape property values, repair needs, service access, and neighborhood vulnerability around tangled titles.",
        "related_interview_themes": ["black_butterfly_geography", "deferred_maintenance"],
    },
    {
        "id": "myth_automatic_transfer",
        "label": "Myth that ownership automatically transfers",
        "level": "Societal Determinants",
        "type": "Barrier",
        "description": "Residents may believe that living in the home, being the adult child, or receiving a verbal promise means they own the property.",
        "related_interview_themes": ["inheritance_myth", "oral_wishes_not_enough"],
    },
    {
        "id": "myth_estate_planning_wealthy",
        "label": "Myth that estate planning is only for wealthy people",
        "level": "Societal Determinants",
        "type": "Barrier",
        "description": "The language of 'estate planning' may sound irrelevant to modest-income homeowners even when their home is their largest asset.",
        "related_interview_themes": ["estate_planning_language", "estate_planning_avoidance"],
    },
    {
        "id": "digital_divide",
        "label": "Digital divide",
        "level": "Societal Determinants",
        "type": "Barrier",
        "description": "Older adults may be excluded from online legal, housing, and government resources because forms, emails, uploads, or web portals are difficult to use.",
        "related_interview_themes": ["digital_divide", "document_collection_burden"],
    },
    {
        "id": "racialized_housing_inequality",
        "label": "Racialized housing inequality and Black Butterfly geography",
        "level": "Societal Determinants",
        "type": "Barrier",
        "description": "Tangled titles are linked to long-term patterns of racialized disinvestment, Black homeownership, wealth extraction, and neighborhood-level inequality.",
        "related_interview_themes": ["black_butterfly_geography", "racialized_wealth_loss"],
    },
    {
        "id": "community_legal_clinics",
        "label": "Community legal clinics",
        "level": "Societal Determinants",
        "type": "Facilitator",
        "description": "Local clinics, fairs, and outreach events can bring estate planning and title-clearing help into the neighborhoods where residents live.",
        "related_interview_themes": ["community_clinics", "door_to_door_outreach"],
    },
    {
        "id": "probate_court_navigator",
        "label": "Probate-court community navigator program",
        "level": "Community Level Factors",
        "type": "Facilitator",
        "description": "A navigator program connected to probate court could help residents understand estate steps, documents, deadlines, and referrals before cases stall.",
        "related_interview_themes": ["knowledge_gap", "administrative_burden"],
    },
    {
        "id": "media_testimonial_campaigns",
        "label": "Media and testimonial campaigns",
        "level": "Community Level Factors",
        "type": "Facilitator",
        "description": "Resident stories, public media, and testimonial campaigns can make tangled titles visible and reduce confusion before households reach crisis.",
        "related_interview_themes": ["community_outreach", "information_gap"],
    },
    {
        "id": "coalition_letters",
        "label": "Coalition letters and cross-sector advocacy",
        "level": "Community Level Factors",
        "type": "Facilitator",
        "description": "Coalition letters and shared advocacy can align legal, housing, community, and policy organizations around the same intervention agenda.",
        "related_interview_themes": ["referral_gap", "community_outreach", "holistic_legal_services"],
    },
]


INTERVIEW_THEMES = [
    {
        "id": "title_blocks_equity",
        "title": "Tangled titles block equity, ownership rights, and housing stability",
        "level": "Central Issue",
        "short_summary": "Tangled titles prevent residents from using home equity, accessing repair funds, defending ownership, or leveraging intergenerational assets.",
        "key_quotes": [
            "Descendants can't use the property, or whoever's living at that property can't use the property, can't access the equity because of some sort of title issue.",
            "They have for decades have not been able to get a home repair, take out a mortgage on that property to fix something, take out a mortgage to send their kid to school; they can't access that equity and that money.",
        ],
        "related_power_nodes": ["tangled_titles", "high_cost_title_clearing", "owner_occupied_protection_gap", "housing_affordability_tradeoff", "reparations_commission_remediation"],
        "implications": "Frame tangled titles as a housing stability and wealth preservation issue, not only a paperwork issue.",
    },
    {
        "id": "crisis_visibility",
        "title": "Tangled titles are often invisible until a crisis or application exposes them",
        "level": "Individual",
        "short_summary": "Many residents learn about tangled titles only when they apply for home repair, receive a tax sale notice, face foreclosure, or interact with a service provider.",
        "key_quotes": [
            "Most people are seeing a symptom usually.",
            "They really find out that there's a big problem usually when they're trying to go access home equity.",
            "Most of our tangled title clients, most of them, not all of them, come to us for something else.",
        ],
        "related_power_nodes": ["housing_service_organizations", "tax_sale_system", "legal_service_organizations", "referral_network"],
        "implications": "Home repair programs, tax sale prevention, and housing counseling should screen for title issues.",
    },
    {
        "id": "knowledge_gap",
        "title": "Residents often do not know what legal steps are required after death",
        "level": "Individual",
        "short_summary": "Many residents do not know about probate, estate administration, deed transfer, or the Register of Wills.",
        "key_quotes": [
            "People just don't know what they don't know.",
            "People don't even know they need to go to the Register of Wills.",
            "There's just no knowledge out there about, like, then what?",
        ],
        "related_power_nodes": ["lack_of_knowledge", "register_of_wills", "information_gap", "probate_process", "probate_court_navigator", "media_testimonial_campaigns"],
        "implications": "Education should explain what happens after a homeowner dies, using plain language and local examples.",
    },
    {
        "id": "inheritance_myth",
        "title": "Living in the home or being family does not automatically create legal ownership",
        "level": "Societal",
        "short_summary": "Residents may assume they inherited the home automatically because they live there, paid bills, or were verbally promised the home.",
        "key_quotes": [
            "They assume because they were the adult child living in the property that they automatically inherited it, which is not true.",
            "They know that their mom is on the deed. But they assume that they are the owner and it's fine.",
            "I inherited this house because my mom told me it's gonna be mine, and then when they go to pay the bill and reach out for assistance, they can't because the deed is actually not in their name.",
        ],
        "related_power_nodes": ["myth_automatic_transfer", "maryland_intestacy_law", "not_engaged_estate_planning", "legal_paperwork_to_titled_owner"],
        "implications": "Public education should directly address the myth of automatic inheritance.",
    },
    {
        "id": "estate_planning_avoidance",
        "title": "Estate planning is delayed by cost, fear, language, and cultural discomfort",
        "level": "Individual",
        "short_summary": "People may avoid estate planning because death is hard to discuss, legal services are costly, and the term 'estate' feels irrelevant or elite.",
        "key_quotes": [
            "I run into a lot of them that don't even like talking about death, or talking about assets.",
            "An estate? I do not have an estate. I own a home, but I do not have an estate.",
            "The word estate feels like Downton Abbey.",
        ],
        "related_power_nodes": ["not_engaged_estate_planning", "myth_estate_planning_wealthy", "costly_process", "engagement_estate_planning"],
        "implications": "Use plain language such as 'protecting your home,' 'who gets the house,' or 'home transfer planning.'",
    },
    {
        "id": "legal_cost_barrier",
        "title": "Legal and administrative costs stop residents from clearing title",
        "level": "Economic",
        "short_summary": "Probate, title clearing, heir outreach, legal consultation, and document preparation can be expensive and intimidating.",
        "key_quotes": [
            "It can be expensive to access estate administration services, probate, to get on the deed.",
            "That level of outreach that is mandated by the court and the law does increase your legal costs, does increase your research costs.",
        ],
        "related_power_nodes": ["costly_process", "high_cost_title_clearing", "probate_process", "fixed_income_seniors"],
        "implications": "Free or low-cost legal services and simplified transfer tools are critical.",
    },
    {
        "id": "administrative_burden",
        "title": "The process is cognitively and logistically burdensome",
        "level": "Structural",
        "short_summary": "Even when residents learn what to do, probate and title clearing can require time, paperwork, transportation, technology, and emotional capacity.",
        "key_quotes": [
            "Going through an administrative process is one more giant thing to have to deal with.",
            "Transportation is a big issue.",
            "For home repair you need to have your deed, electricity bills or water bills, mortgage papers, and SSN and ID cards to be able to qualify for programs.",
        ],
        "related_power_nodes": ["digital_and_document_burden", "register_of_wills", "probate_process", "digital_divide", "probate_court_navigator"],
        "implications": "Services should include navigation, document support, and in-person assistance.",
    },
    {
        "id": "family_conflict",
        "title": "Family conflict can turn ownership into a housing crisis",
        "level": "Interpersonal",
        "short_summary": "Sibling disagreements, competing claims, and family conflict can block repairs, sales, title clearing, or stable residence.",
        "key_quotes": [
            "It can really fragment a family.",
            "Sometimes siblings don't get along.",
            "One's trying to force one out of the house.",
        ],
        "related_power_nodes": ["family_disagreement", "no_clear_heir", "partition_and_forced_sale", "mediation_services"],
        "implications": "Title clearing often requires family mediation, not only legal paperwork.",
    },
    {
        "id": "joint_decision_burden",
        "title": "Joint ownership requires consensus that families may not be able to reach",
        "level": "Interpersonal",
        "short_summary": "When multiple heirs have legal interests, one person's repair, sale, or transfer decision may require consent from others.",
        "key_quotes": [
            "In practice, it's a bit of a nightmare, because siblings need to be able to make joint decisions.",
            "If they can't come to consensus, then in many ways the property may sit in limbo.",
        ],
        "related_power_nodes": ["family_disagreement", "no_clear_heir", "family_cohesion", "mediation_services"],
        "implications": "Programs should anticipate multi-heir decision-making and contested title cases.",
    },
    {
        "id": "home_repair_gateway",
        "title": "Home repair programs are a major gateway for discovering tangled titles",
        "level": "Community",
        "short_summary": "Residents often learn about title problems when they apply for repair funding and are told they need clear title or consent from all deed holders.",
        "key_quotes": [
            "One of the conditions of receiving home repair funding in the city, in particular, is that you have to have a clear title.",
            "It's impossible for them, for legal reasons, to actually move on making those repairs.",
            "It can be a dead-on-arrival situation.",
        ],
        "related_power_nodes": ["housing_service_organizations", "owner_occupied_protection_gap", "repair_grant_estate_planning_link", "referral_network"],
        "implications": "Repair programs should be paired with legal screening and title-clearing support.",
    },
    {
        "id": "deferred_maintenance",
        "title": "Tangled titles contribute to unsafe housing and deferred maintenance",
        "level": "Economic",
        "short_summary": "When people cannot access repairs, homes deteriorate, creating health, safety, and vacancy risks.",
        "key_quotes": [
            "You can get your leaky roof fixed. You can get maybe some accessibility upgrades.",
            "These homes could either be condemned, or honestly, just decayed to a point that these people can no longer live in them.",
        ],
        "related_power_nodes": ["rising_repair_costs", "housing_service_organizations", "housing_affordability_tradeoff", "tax_sale_system"],
        "implications": "Tangled titles should be treated as part of housing quality, public health, and vacancy prevention.",
    },
    {
        "id": "shelter_security",
        "title": "The home is shelter first, not just an asset",
        "level": "Central Issue",
        "short_summary": "For many residents, the family home is the only affordable housing option. Losing it can mean displacement or homelessness.",
        "key_quotes": [
            "One of the most important things that people are actually getting from these homes is shelter.",
            "I couldn't afford rent if I can't live at this house.",
            "$4,000 for a whole year to live at a house is much less than the rental cost would be.",
        ],
        "related_power_nodes": ["housing_affordability_tradeoff", "tax_sale_system", "tangled_titles", "fixed_income_seniors"],
        "implications": "Present tangled titles as an affordable housing preservation issue.",
    },
    {
        "id": "tax_sale_vulnerability",
        "title": "Tangled titles increase vulnerability to tax sale and foreclosure",
        "level": "Structural",
        "short_summary": "Residents may not receive the right notices, may lack legal standing, or may lose owner-occupied protections when property taxes or bills become overdue.",
        "key_quotes": [
            "Tax sale is where they collect overdue property taxes, and that collection of overdue property taxes can actually lead to a foreclosure on the home.",
            "All of the legal paperwork is addressed to the homeowner.",
            "They also usually aren't getting the benefits of being a homeowner and an owner occupied property.",
        ],
        "related_power_nodes": ["tax_sale_system", "legal_paperwork_to_titled_owner", "owner_occupied_protection_gap", "annual_tax_lien_sales"],
        "implications": "Tax sale prevention should include title screening and legal representation.",
    },
    {
        "id": "service_eligibility_barrier",
        "title": "Title defects exclude residents from public benefits and housing supports",
        "level": "Structural",
        "short_summary": "Residents may be unable to obtain home repair assistance, property tax credits, water bill discounts, or other support because their name is not on the deed.",
        "key_quotes": [
            "They can't get property tax credits, other financial assistance that would help keep the property taxes affordable, or home repairs assistance to help maintain the property properly.",
            "Because their name is not on the deed, they're not eligible.",
        ],
        "related_power_nodes": ["owner_occupied_protection_gap", "housing_service_organizations", "stop_oppressive_seizures_fund", "legal_service_organizations"],
        "implications": "Eligibility systems should have a clear pathway for residents with tangled titles.",
    },
    {
        "id": "holistic_legal_services",
        "title": "Holistic legal services can catch tangled titles through multiple entry points",
        "level": "Community",
        "short_summary": "Legal providers often identify title issues when clients seek help for taxes, estate planning, foreclosure, repairs, or other housing problems.",
        "key_quotes": [
            "We offer estate planning, mortgage foreclosure, tax sale prevention. We try to cast that net so wide that it increases the opportunity to catch tangled titles.",
            "We research every client, and then we're like, hey, you have a tangled title, do you want us to help you fix that?",
        ],
        "related_power_nodes": ["legal_service_organizations", "mvls", "pro_bono_resource_center", "referral_network"],
        "implications": "Any organization working with homeowners should ask whether the resident is on title.",
    },
    {
        "id": "community_outreach",
        "title": "Outreach should go to residents rather than waiting for residents to find services",
        "level": "Community",
        "short_summary": "Trusted outreach through neighborhood associations, block captains, clinics, community fairs, and door knocking can reach residents before crisis.",
        "key_quotes": [
            "Instead of waiting for people to come to you, go to them.",
            "We're constantly going to neighborhood association meetings, connecting with new partners, and going to neighborhood association meetings.",
            "This year we focused more on us organizing door knocking.",
        ],
        "related_power_nodes": ["neighborhood_associations", "block_captains", "community_legal_clinics", "baltimore_neighborhood_indicators_alliance", "media_testimonial_campaigns", "coalition_letters"],
        "implications": "Outreach should be proactive, place-based, and locally trusted.",
    },
    {
        "id": "referral_gap",
        "title": "Referral systems need tracking and warm handoffs",
        "level": "Community",
        "short_summary": "Giving someone a phone number may not be enough. Residents need case navigation and follow-through between housing programs and legal services.",
        "key_quotes": [
            "You're just giving them a number and saying contact them, versus saying I'm going to make a connection for you with this particular person in this particular organization so that your case can move forward.",
            "There's no tracking of whether, if you've referred people out to legal providers, they're coming back into the pipeline of the home repair services.",
        ],
        "related_power_nodes": ["referral_network", "housing_service_organizations", "legal_service_organizations", "stop_oppressive_seizures_fund", "coalition_letters"],
        "implications": "Build warm handoff workflows and track whether legal referrals resolve the barrier.",
    },
    {
        "id": "data_driven_outreach",
        "title": "Data can identify neighborhoods and properties at higher risk",
        "level": "Structural",
        "short_summary": "Administrative records, property records, death records, repair requests, social service records, and neighborhood data could support proactive outreach.",
        "key_quotes": [
            "It was just a comparison of current property records with public death records; how many of the death records are still on a property. We found like 3000.",
            "If you overlay all those things together, maybe that is the population we should go out to.",
            "More rigorous analysis would be really helpful.",
        ],
        "related_power_nodes": ["baltimore_neighborhood_indicators_alliance", "neighborhood_associations", "block_captains", "racialized_housing_inequality"],
        "implications": "Use data to prioritize outreach while protecting privacy and avoiding punitive targeting.",
    },
    {
        "id": "black_butterfly_geography",
        "title": "Tangled titles are spatially and racially patterned",
        "level": "Societal",
        "short_summary": "Interviewees connect tangled titles with lower-income homeowners, Black neighborhoods, seniors, long-time owners, and the Black Butterfly geography of Baltimore.",
        "key_quotes": [
            "Lower-income communities and communities that are predominantly minority communities are affected at higher rates than other communities.",
            "Most of the times it is the Black Butterfly region.",
            "Our population is about 90% Black and mostly seniors.",
        ],
        "related_power_nodes": ["racialized_housing_inequality", "baltimore_neighborhood_indicators_alliance", "fixed_income_seniors", "annual_tax_lien_sales", "historic_modern_segregation", "eminent_domain_asset_forfeiture", "reparations_commission_remediation"],
        "implications": "Frame tangled titles as a racialized housing and wealth issue, not only an individual paperwork failure.",
    },
    {
        "id": "fixed_income_seniors",
        "title": "Older adults on fixed incomes face compounded risk",
        "level": "Economic",
        "short_summary": "Seniors may have long-term homeownership and deep neighborhood roots, but limited income for legal help, taxes, or repairs.",
        "key_quotes": [
            "People often seeking assistance are elderly people on fixed incomes.",
            "The cost of repair work, contractors, and even materials like wood has gone up over the last few years, while their income has stayed pretty steady.",
        ],
        "related_power_nodes": ["fixed_income_seniors", "rising_repair_costs", "high_cost_title_clearing", "digital_divide"],
        "implications": "Older homeowners need low-barrier, in-person, affordable title and repair support.",
    },
    {
        "id": "preventive_planning",
        "title": "Prevention is easier while the homeowner is still alive",
        "level": "Policy",
        "short_summary": "Wills, transfer-on-death deeds, life estate deeds, and estate planning can prevent tangled titles before heirs face probate complexity.",
        "key_quotes": [
            "Do this work while they are still alive.",
            "It gets much stickier when people are deceased.",
            "If people had their wills and they had life estate deeds, this would not be an issue.",
        ],
        "related_power_nodes": ["engagement_estate_planning", "transfer_on_death_deed", "repair_grant_estate_planning_link", "community_legal_clinics"],
        "implications": "Pair prevention with home repair, tax credit, senior service, and community outreach programs.",
    },
    {
        "id": "transfer_on_death_deed",
        "title": "Transfer-on-death deeds are a promising policy facilitator",
        "level": "Policy",
        "short_summary": "Simplified deed tools may reduce dependence on expensive attorneys and probate after death.",
        "key_quotes": [
            "The law that just passed makes it so much easier. Now it's just a document that you can fill out, and you don't need an attorney for it.",
            "Now it's just a document.",
        ],
        "related_power_nodes": ["transfer_on_death_deed", "engagement_estate_planning", "high_cost_title_clearing", "not_engaged_estate_planning"],
        "implications": "Explain transfer-on-death deeds as an example of policy simplification, not as a universal solution.",
    },
    {
        "id": "repair_grant_policy",
        "title": "Repair grants could be linked to title clearing and estate planning",
        "level": "Policy",
        "short_summary": "Public repair funding could become an opportunity to encourage estate planning and clear title before crisis.",
        "key_quotes": [
            "In exchange for receiving repair grant money, we can require or strongly encourage them to do estate planning.",
            "Can we offer a service that helps build generational wealth by supporting estate planning while people are still alive?",
        ],
        "related_power_nodes": ["repair_grant_estate_planning_link", "housing_service_organizations", "engagement_estate_planning", "legal_service_organizations"],
        "implications": "Build title clearing and estate planning into repair grant workflows.",
    },
]


INTERVENTION_LEVERAGE_POINTS = [
    ("Preventive estate planning", ["preventive_planning", "transfer_on_death_deed", "estate_planning_avoidance"]),
    ("Home repair program screening", ["home_repair_gateway", "repair_grant_policy", "service_eligibility_barrier"]),
    ("Legal aid and title clearing", ["holistic_legal_services", "legal_cost_barrier", "administrative_burden"]),
    ("Mediation for family conflict", ["family_conflict", "joint_decision_burden"]),
    ("Warm handoffs and case navigation", ["referral_gap", "crisis_visibility"]),
    ("Probate-court navigation", ["knowledge_gap", "administrative_burden"]),
    ("Media and testimonial campaigns", ["community_outreach", "knowledge_gap"]),
    ("Coalitional advocacy", ["referral_gap", "community_outreach", "holistic_legal_services"]),
    ("Policy reform and reparations-oriented remediation", ["transfer_on_death_deed", "black_butterfly_geography", "tax_sale_vulnerability"]),
    ("Data-driven outreach", ["data_driven_outreach", "community_outreach", "black_butterfly_geography"]),
    ("Tax sale prevention", ["tax_sale_vulnerability", "shelter_security"]),
    ("Digital and document assistance", ["administrative_burden", "fixed_income_seniors"]),
]

QUALITATIVE_SLIDE_RESOURCE_LINKS = [
    {
        "label": "Baltimore City free legacy planning program",
        "focus": "Asset protection and intergenerational wealth planning",
        "url": "https://www.baltimorecity.gov/moed/news/baltimore-city-launches-free-legacy-planning-program-to-help-increase-asset-protection-and-intergenerational-wealth",
    },
    {
        "label": "Pro Bono Resource Center HPP estate planning clinic",
        "focus": "Estate planning and document preparation",
        "url": "https://probonomd.org/eb_item/hpp-estate-planning-clinic-baltimore-city/",
    },
    {
        "label": "Pratt Library estate planning pro bono clinic",
        "focus": "Public library-based legal document preparation",
        "url": "https://calendar.prattlibrary.org/event/estate-planning-pro-bono-document-preparation-clinic",
    },
    {
        "label": "MVLS estate planning clinics and seminars",
        "focus": "Legal aid and preventive planning",
        "url": "https://mvlslaw.org/upcoming-estate-planning-clinics-seminars-maryland/",
    },
    {
        "label": "Johns Hopkins estate planning clinic",
        "focus": "Community-based estate planning outreach",
        "url": "https://www.eventbrite.com/e/estate-planning-clinic-tickets-1978445245989",
    },
    {
        "label": "Greater Baltimore Urban League estate planning workshop",
        "focus": "Neighborhood-based estate planning education",
        "url": "https://www.facebook.com/gbulorg1924/posts/planning-for-the-future-starts-todayjoin-the-greater-baltimore-urban-league-in-p/1270806085166466/",
    },
    {
        "label": "Community Mediation Maryland",
        "focus": "Low-cost family and community mediation",
        "url": "https://mdmediation.org/need-mediation/",
    },
    {
        "label": "Baltimore Community Mediation Center",
        "focus": "Family and neighborhood conflict resolution",
        "url": "https://bcmccatalyst.gatsbyjs.io/",
    },
    {
        "label": "Restorative Response Baltimore",
        "focus": "Community mediation and restorative practices",
        "url": "https://www.restorativeresponse.org/",
    },
    {
        "label": "Baltimore City Financial Empowerment Center",
        "focus": "Financial counseling and navigation support",
        "url": "https://www.baltimorecity.gov/moed/financial-empowerment-center",
    },
    {
        "label": "Baltimore City tax sale prevention resources",
        "focus": "Tax sale prevention and homeowner stabilization",
        "url": "https://www.baltimorecity.gov/dhcd/resources-for-homeowners/tax-sale-prevention",
    },
    {
        "label": "West Baltimore estate planning outreach",
        "focus": "Place-based estate planning outreach",
        "url": "https://www.hubwestbaltimore.org/estate-planning-outreach",
    },
]

GLOSSARY_TERMS = [
    ("Title", "The legal right to own and control a property.", "Tangled titles happen when title records do not match who lives in or cares for the home."),
    ("Deed", "A recorded legal document that shows who owns a property.", "Many barriers begin when the deed still lists someone who died or moved away."),
    ("On the deed", "Having your name listed as an owner in the recorded deed.", "Programs often require the applicant to be on the deed before help can move forward."),
    ("Clear title", "A title record with no unresolved ownership problems, liens, or competing claims.", "Clear title makes repair grants, tax credits, refinancing, and transfer easier."),
    ("Tangled title", "A mismatch between formal ownership records and lived family arrangements.", "The resident may act like the owner but not be recognized as the legal owner."),
    ("Heirs' property", "Property inherited by multiple heirs, often without a clear recorded transfer.", "Multiple heirs can create fractional interests and decision-making barriers."),
    ("Estate", "The property, money, and legal interests someone leaves after death.", "A modest family home can still be an estate that needs legal handling."),
    ("Estate planning", "Planning what happens to property after death.", "Planning before death can prevent heirs from facing a tangled title later."),
    ("Will", "A legal document saying who should receive someone's property after death.", "A will can clarify wishes, though some property transfer steps may still be needed."),
    ("Probate", "A court-supervised process for handling property after someone dies.", "Probate is often needed before a deceased owner's home can transfer to heirs."),
    ("Estate administration", "The practical and legal work of managing a deceased person's estate.", "It can involve paperwork, notices, debts, heirs, and deed transfer."),
    ("Register of Wills", "A local office involved in opening estates and probate matters.", "Residents may not know this office is relevant after a homeowner dies."),
    ("Personal representative", "The person authorized to manage an estate during probate.", "This role can be necessary before title problems can be resolved."),
    ("Executor", "A person named in a will to carry out the deceased person's wishes.", "An executor may help move the legal process forward if a valid will exists."),
    ("Transfer-on-death deed", "A deed tool that can name who receives property after death.", "It may prevent some probate complexity when used correctly before death."),
    ("Life estate deed", "A deed arrangement allowing one person to live in a property during life while naming who receives it later.", "It can be a planning tool, but residents need legal guidance before using it."),
    ("Heir", "A person legally entitled to inherit from someone who died.", "Several heirs may need to agree before a title issue can be resolved."),
    ("Beneficiary", "A person named to receive property or benefits.", "A beneficiary may not have usable ownership rights until legal transfer steps happen."),
    ("Property tax", "A local tax charged on real estate.", "Unpaid taxes can create tax sale and foreclosure risk."),
    ("Delinquent taxes", "Property taxes that are overdue.", "Delinquency can trigger notices, fees, liens, or tax sale."),
    ("Tax sale", "A process where unpaid taxes or charges can be sold as a lien.", "For tangled title residents, tax sale can threaten a home they rely on for shelter."),
    ("Tax lien", "A legal claim against property for unpaid taxes or charges.", "A lien can move the property closer to foreclosure if unresolved."),
    ("Foreclosure", "A legal process that can result in losing a property.", "Tax sale or mortgage problems can become foreclosure risks."),
    ("Owner-occupied", "A property where the owner lives in the home.", "Residents not on title may lose protections or credits tied to owner-occupancy."),
    ("Home repair grant", "Public or nonprofit funding to help fix a home.", "Clear title is often required before repair money can be used."),
    ("Eligibility", "The rules that decide who can receive a program or benefit.", "Tangled titles often block eligibility even when the resident needs help."),
    ("Legal aid", "Free or low-cost legal help for people who cannot afford private attorneys.", "Legal aid can help with probate, deeds, tax sale prevention, and title clearing."),
    ("Joint ownership", "Ownership shared by more than one person.", "Joint owners may all need to agree before repairs, sale, or transfer."),
    ("Fractional interest", "A partial ownership share in a property.", "Small shares can still affect decisions and create vulnerability to forced sale."),
    ("Partition", "A legal action to divide or sell jointly owned property.", "Partition can become a threat when heirs disagree or outside buyers acquire shares."),
    ("Forced sale", "A sale pushed through legal or financial pressure rather than family agreement.", "Families can lose a home when ownership is unresolved or contested."),
    ("Speculator", "An investor seeking profit from property or ownership interests.", "Speculators may exploit unclear ownership or tax sale vulnerability."),
    ("Black Butterfly", "A term describing Baltimore's pattern of predominantly Black neighborhoods across the east and west sides.", "Tangled titles overlap with racialized housing disinvestment and wealth extraction."),
    ("Redlining", "Historic discrimination that denied credit and investment to Black neighborhoods.", "Its legacy shapes property values, repair needs, and neighborhood risk today."),
    ("Deferred maintenance", "Repairs that are delayed because money, authority, or access is missing.", "Tangled titles can delay repairs until homes become unsafe or uninhabitable."),
    ("Warm handoff", "A referral where one provider actively connects a resident to another provider.", "Warm handoffs are more reliable than giving residents a phone number and hoping they can navigate alone."),
]

TITLE_COMPARISON = {
    "clear": [
        "Name on deed",
        "Legal ownership is recognized",
        "Can access repair grants and tax credits more easily",
        "Receives formal notices correctly",
        "Can transfer, refinance, or use home equity more easily",
        "Lower risk of service exclusion",
    ],
    "tangled": [
        "Resident's name may not be on deed",
        "Legal ownership does not match lived ownership",
        "Repair grants or tax credits may be blocked",
        "Notices may go to deceased or absent titled owners",
        "Family conflict or unresolved inheritance may remain",
        "Higher risk of tax sale, foreclosure, vacancy, or displacement",
    ],
}

PROBLEM_PATHWAY_DETAIL = [
    "Homeowner dies or title becomes outdated",
    "No probate or deed transfer",
    "Legal ownership does not match lived ownership",
    "Resident is not recognized as the legal owner",
    "Repair grants, tax credits, water discounts, or legal protections may be blocked",
    "Deferred maintenance, unpaid bills, family conflict, or tax delinquency can accumulate",
    "Tax sale, foreclosure, vacancy, displacement, or loss of intergenerational wealth",
]

QUOTE_WALL_ITEMS = [
    ("Invisible until crisis", "Most people are seeing a symptom usually.", "crisis_visibility", "housing_service_organizations"),
    ("Invisible until crisis", "Most of our tangled title clients, most of them, not all of them, come to us for something else.", "crisis_visibility", "referral_network"),
    ("Ownership mismatch", "They assume because they were the adult child living in the property that they automatically inherited it, which is not true.", "inheritance_myth", "myth_automatic_transfer"),
    ("Ownership mismatch", "They know that their mom is on the deed. But they assume that they are the owner and it's fine.", "inheritance_myth", "legal_paperwork_to_titled_owner"),
    ("Home repair barriers", "One of the conditions of receiving home repair funding in the city, in particular, is that you have to have a clear title.", "home_repair_gateway", "housing_service_organizations"),
    ("Home repair barriers", "It can be a dead-on-arrival situation.", "home_repair_gateway", "owner_occupied_protection_gap"),
    ("Family conflict", "It can really fragment a family.", "family_conflict", "family_disagreement"),
    ("Family conflict", "If they can't come to consensus, then in many ways the property may sit in limbo.", "joint_decision_burden", "no_clear_heir"),
    ("Shelter and wealth", "One of the most important things that people are actually getting from these homes is shelter.", "shelter_security", "housing_affordability_tradeoff"),
    ("Shelter and wealth", "Descendants can't use the property, or whoever's living at that property can't use the property, can't access the equity because of some sort of title issue.", "title_blocks_equity", "tangled_titles"),
    ("Legal and administrative burden", "Going through an administrative process is one more giant thing to have to deal with.", "administrative_burden", "probate_process"),
    ("Legal and administrative burden", "People don't even know they need to go to the Register of Wills.", "knowledge_gap", "register_of_wills"),
    ("Structural inequality", "Most of the times it is the Black Butterfly region.", "black_butterfly_geography", "racialized_housing_inequality"),
    ("Structural inequality", "Lower-income communities and communities that are predominantly minority communities are affected at higher rates than other communities.", "black_butterfly_geography", "annual_tax_lien_sales"),
    ("Community outreach", "Instead of waiting for people to come to you, go to them.", "community_outreach", "community_legal_clinics"),
    ("Community outreach", "You're just giving them a number and saying contact them, versus saying I'm going to make a connection for you with this particular person in this particular organization so that your case can move forward.", "referral_gap", "referral_network"),
]

TRANSCRIPT_RECURRING_TERMS = [
    ("title", 122),
    ("deed", 51),
    ("repair", 48),
    ("family", 43),
    ("will", 39),
    ("estate planning", 34),
    ("home repair", 28),
    ("income", 20),
    ("property tax", 17),
    ("heirs", 15),
    ("death", 14),
    ("siblings", 13),
    ("vacant housing", 13),
    ("heirs property", 12),
    ("wealth", 12),
    ("tax sale", 11),
    ("asset", 11),
    ("foreclosure", 9),
    ("probate", 8),
    ("equity", 7),
    ("seniors", 7),
    ("legal aid", 6),
    ("mediation", 6),
    ("shelter", 6),
    ("renters", 5),
    ("city innovation", 5),
    ("tax credit", 4),
    ("repair grant", 4),
    ("Black Butterfly", 3),
    ("racialized inequality", 3),
    ("Register of Wills", 3),
    ("transportation", 3),
    ("referral", 3),
    ("consensus", 3),
    ("Pro Bono Resource Center", 3),
    ("MVLS", 2),
    ("fixed income", 2),
    ("neighborhood association", 2),
    ("civic designer", 2),
    ("warm handoff", 1),
    ("transfer-on-death deed", 1),
    ("life estate deed", 1),
    ("owner-occupied", 1),
    ("housing stability", 1),
]

EVIDENCE_DOMAINS = {
    "Knowledge and estate planning": ["lack_of_knowledge", "not_engaged_estate_planning", "engagement_estate_planning", "transfer_on_death_deed", "myth_estate_planning_wealthy", "information_gap", "myth_automatic_transfer"],
    "Family and heirs": ["family_disagreement", "no_clear_heir", "partition_and_forced_sale", "family_cohesion", "mediation_services", "maryland_intestacy_law"],
    "Home repair and service eligibility": ["housing_service_organizations", "owner_occupied_protection_gap", "repair_grant_estate_planning_link", "digital_and_document_burden"],
    "Legal aid and probate": ["legal_service_organizations", "mvls", "pro_bono_resource_center", "probate_process", "register_of_wills", "costly_process", "high_cost_title_clearing"],
    "Tax sale and foreclosure": ["tax_sale_system", "legal_paperwork_to_titled_owner", "annual_tax_lien_sales", "stop_oppressive_seizures_fund"],
    "Community outreach": ["neighborhood_associations", "block_captains", "community_legal_clinics", "referral_network"],
    "Data-driven targeting": ["baltimore_neighborhood_indicators_alliance"],
    "Structural and racialized inequality": ["racialized_housing_inequality", "fixed_income_seniors", "rising_repair_costs", "housing_affordability_tradeoff", "vulnerability_to_speculators"],
}

SYSTEM_TOUCHPOINT_LANES = [
    {
        "lane": "Resident / household",
        "examples": ["homeowner", "heir living in the home", "older adult", "fixed-income resident"],
        "encounters": ["after a death in the family", "when a repair becomes urgent", "when bills become hard to manage"],
    },
    {
        "lane": "Family / interpersonal actors",
        "examples": ["siblings", "heirs", "extended family", "absent deed holders", "family members with fractional interests"],
        "encounters": ["when signatures are needed", "when heirs disagree", "when a property may be sold or transferred"],
    },
    {
        "lane": "Community support actors",
        "examples": ["neighborhood associations", "block captains", "community clinics", "trusted local leaders", "coalitions", "media campaigns"],
        "encounters": ["during outreach", "at community meetings", "when residents need trusted guidance", "when organizations coordinate public advocacy"],
    },
    {
        "lane": "Housing and legal service providers",
        "examples": ["home repair programs", "housing counselors", "legal aid", "MVLS", "Pro Bono Resource Center", "Stop Oppressive Seizures Fund"],
        "encounters": ["when applying for a repair grant", "when seeking legal aid", "when a referral needs follow-through"],
    },
    {
        "lane": "Formal legal and administrative systems",
        "examples": ["Register of Wills", "probate process", "courts", "deed recording", "estate administration"],
        "encounters": ["after a death", "when opening an estate", "when deed records need correction"],
    },
    {
        "lane": "Tax and municipal systems",
        "examples": ["property tax office", "water bills", "municipal charges", "tax sale system", "foreclosure process"],
        "encounters": ["when receiving a tax delinquency notice", "when charges accumulate", "when tax sale risk appears"],
    },
    {
        "lane": "Data and spatial targeting actors",
        "examples": ["BNIA", "property records", "death records", "repair request data", "neighborhood indicators"],
        "encounters": ["when identifying outreach areas", "when matching records", "when targeting services proactively"],
    },
    {
        "lane": "Market actors",
        "examples": ["tax lien buyers", "speculators", "investors", "property purchasers"],
        "encounters": ["when liens are sold", "when fractional interests are targeted", "when a property becomes vulnerable to sale"],
    },
]

TASHA_JOURNEY_ASSET_DIR = "assets/case_study/tasha_journey"
TASHA_JOURNEY_OVERVIEW_IMAGE = {
    "image": f"{TASHA_JOURNEY_ASSET_DIR}/tasha_00_overview_system_tangle.png",
    "alt": "Tasha Johnson outside a West Baltimore rowhouse with deed, tax bill, legal papers, repair assistance, and tax sale risk shown around the home.",
    "caption": "Composite overview image for Tasha Johnson's tangled-title journey.",
}

TASHA_PROFILE = {
    "name": "Tasha Johnson",
    "age": "35 years old",
    "race_ethnicity": "Black/African-American",
    "hometown": "West Baltimore, Maryland",
    "job": "Front desk receptionist at Freedman's Health Clinic",
    "income": "$16.61/hour, about $34,545/year",
    "household_role": "Head of household",
    "scenario_location": "Baltimore, Maryland",
    "problem": "Tangled title, property tax burden, tax sale risk, and first-generation homeownership without clear transfer documentation",
    "resources_needed": "Funding for legal costs, clear ownership title, estate planning support, a notarized will to prevent future title problems, financial counseling, and emotional support",
}

TASHA_CASE_STUDY_SOURCES = [
    {
        "label": "Baltimore Banner, Frederick Williams tax sale case",
        "date": "March 24, 2024",
        "url": "https://www.thebanner.com/community/housing/frederick-williams-tax-sale-baltimore-GCFNRESPTNFJPMOINW7Y73NP4E/",
        "note": "Used as a real-world reference point for the administrative-delay and tax-sale mechanics in this fictional composite.",
    },
    {
        "label": "Baltimore Banner archived article",
        "date": "April 22, 2024",
        "url": "https://archive.is/B15lj",
        "note": "Background article used for local housing and tax-sale context.",
    },
    {
        "label": "Black Wealth Data Center, Quantifying Tangled Titles",
        "date": "October 2025",
        "url": "https://blackwealthdata.org/about-us/news/post/Quantifying-Tangled-Titles-A-Hidden-Barrier-to-Wealth-Transfer",
        "note": "Used for Baltimore-scale framing on tangled titles, tax sale, neighborhood burden, and locked household wealth.",
    },
    {
        "label": "ZipRecruiter, Front Desk Receptionist Salary in Baltimore, Maryland",
        "date": "May 8, 2026",
        "url": "https://www.ziprecruiter.com/Salaries/Front-Desk-Receptionist-Salary-in-Baltimore,MD",
        "note": "Used to ground the fictional profile's receptionist wage and annual income.",
    },
]

RESIDENT_JOURNEY_STAGES = [
    {
        "id": "family_legacy",
        "title": "Family Legacy and Lived Ownership",
        "image": f"{TASHA_JOURNEY_ASSET_DIR}/tasha_01_family_legacy.png",
        "alt": "Tasha Johnson standing in or near her long-time family home, showing family legacy and hidden title uncertainty.",
        "story_hook": "At home, Tasha is the person who keeps the house going.",
        "narrative": "Tasha is a 35-year-old head of household in West Baltimore who earns $16.61 an hour as a full-time receptionist. The house she calls home is more than shelter; it is a 66-year family legacy and her family's largest financial asset. In daily life, Tasha and four other heirs all have a stake in what happens to the property, so repair, tax, sale, or transfer decisions can become contested even though Tasha is the person keeping the house going. The legal ownership record has not caught up with the family reality.",
        "touchpoint": "Household, family inheritance, deed records",
        "power_map_connection": "Individual level, interpersonal level, estate planning, formal ownership vs lived ownership",
        "barrier": "The problem is mostly invisible because Tasha's grandparents did not have a notarized will or clear transfer documents, so deceased owners remain on the deed.",
        "evidence_note": "Profile details draw from the provided avatar background and salary source. The lack of estate planning reflects the case-study framing around first-generation homeowners, limited knowledge of home transfers, and high legal costs.",
        "source_labels": ["ZipRecruiter", "BWDC"],
    },
    {
        "id": "repair_application_blocked",
        "title": "Repair Need Exposes the Tangled Title",
        "image": f"{TASHA_JOURNEY_ASSET_DIR}/tasha_02_repair_application_blocked.png",
        "alt": "Tasha confronting a home repair problem while her repair assistance application is blocked by unclear title.",
        "story_hook": "The problem does not begin with a lawyer. It begins with a leak.",
        "narrative": "Because Tasha is not legally recognized as the owner, she is invisible to systems designed to support low-income homeowners. Homeowners' tax credits, homestead protections, repair grants, and low-interest repair loans can all become harder to access. Without these protections, taxes can rise sharply over a short period. As the roof or plumbing deteriorates, the repair application reveals what daily life had hidden: she cannot prove that she owns the house.",
        "touchpoint": "Home repair program, housing service provider, deed verification",
        "power_map_connection": "Housing service organizations, service eligibility barrier, owner-occupied protection gap",
        "barrier": "Repair grants, tax credits, and owner-occupied protections may require clear title or proof that the applicant is legally recognized as the homeowner.",
        "evidence_note": "This stage uses the case-study discussion of Homeowners' Tax Credit, Homestead Tax Credit, repair grants, low-interest loans, and the way tangled status can punish low-income residents for a documentation mismatch.",
        "source_labels": ["BWDC", "Baltimore Banner"],
    },
    {
        "id": "tax_payment_admin_delay",
        "title": "Tax Pressure and Administrative Burden",
        "image": f"{TASHA_JOURNEY_ASSET_DIR}/tasha_03_tax_payment_admin_delay.png",
        "alt": "Tasha dealing with property tax paperwork and administrative delays while trying to protect her home.",
        "story_hook": "Trying to fix the problem creates a second problem: paperwork, notices, and systems that do not recognize her.",
        "narrative": "Family disagreement over how to manage the property stalls probate while taxes continue to pressure the household. Tasha scrapes together $13,000 to address outstanding property taxes, but payments, notices, and legal documents remain tied to deceased owners or titled owners rather than to her. Similar to the Frederick Williams tax-sale reporting, even a delay in processing payment can become catastrophic when the title record does not recognize the person trying to save the home.",
        "touchpoint": "Property tax system, municipal charges, payment processing, legal notices",
        "power_map_connection": "Tax sale system, legal paperwork addressed to titled owner, administrative burden",
        "barrier": "Because Tasha is not legally recognized as the owner, tax-sale and foreclosure paperwork may not reach her in time or may not treat her as the person with standing to resolve the problem.",
        "evidence_note": "This stage adapts the administrative-delay logic from reporting on Frederick Williams' Baltimore tax-sale case, including the case-study detail that a check was not cashed for nearly a month, while keeping Tasha fictional.",
        "source_labels": ["Baltimore Banner", "BWDC"],
    },
    {
        "id": "foreclosure_threat",
        "title": "Foreclosure Threat and Loss of Shelter",
        "image": f"{TASHA_JOURNEY_ASSET_DIR}/tasha_04_foreclosure_threat.png",
        "alt": "Tasha standing outside her family home as a foreclosure or tax sale threat becomes real.",
        "story_hook": "By the time the crisis is visible, the home is no longer just a legal issue. It is shelter.",
        "narrative": "The crisis becomes visible when the property is mistakenly sold through tax sale or moves toward foreclosure. Because Tasha's name is not on the deed, she may not receive legal notice in the same way a clear-title owner would. She may only realize the gravity of the situation when a stranger arrives to inspect the house for auction. The home is shelter, family memory, and a pathway to intergenerational stability.",
        "touchpoint": "Tax sale, foreclosure process, market actors, investor or speculator interest",
        "power_map_connection": "Tax sale vulnerability, market actors, housing loss, racialized wealth loss",
        "barrier": "Tangled title turns a paperwork problem into a housing stability crisis and can expose family wealth to tax lien buyers, investors, vacancy, or displacement.",
        "evidence_note": "This stage connects the fictional journey to Baltimore tax-sale reporting and BWDC's framing of tangled titles as a hidden barrier to wealth transfer.",
        "source_labels": ["Baltimore Banner", "BWDC"],
    },
]

TASHA_CASE_STUDY_IMPLICATIONS = [
    "Legal-cost support and title clearing are central needs because Tasha cannot resolve ownership without navigating probate, deed records, and family claims.",
    "Estate planning support, including notarized wills or other transfer tools, can help prevent the same title problem from recurring in the next generation.",
    "Financial and emotional counseling matter because the crisis is not only legal; it affects taxes, repairs, family conflict, stress, and household stability.",
    "Community workshops can bridge the information gap before a home reaches the tax sale list.",
    "BWDC-style data can help identify high-risk census tracts for proactive outreach, while avoiding punitive targeting of residents.",
    "Maryland policy reform could reduce the risk that families lose inherited homes because tax bills, title transfer, and probate systems do not line up.",
    "One reform direction raised by the case study is allowing property to pass to heirs even when tax bills are behind, so tax debt does not automatically block family wealth transfer.",
    "Untangling titles can return substantial equity to residents, potentially unlocking billions in neighborhood wealth over time and helping secure the wealth that families built over decades.",
]

TASHA_BALTIMORE_SCALE_CONTEXT = {
    "tax_sale": "The case study frames Tasha's neighborhood as part of a broader Baltimore pattern where 41,000 properties, mostly in Black neighborhoods, have cycled through the tax sale system since 2016.",
    "locked_assets": "BWDC and Local Wealth Explorer framing connect tangled titles to more than $300 million in locked assets across Baltimore, wealth that could otherwise support generational transfer, home repair, or small-business formation.",
    "vacancy_cost": "When inherited homes are lost or left unresolved, they can become vacant, contributing to lost city revenue, direct public costs, and neighborhood instability.",
}

SOLUTION_CATEGORIES = [
    ("Upstream prevention", ["plain-language estate planning", "transfer-on-death deeds", "wills and life estate deeds", "estate planning while the homeowner is alive"]),
    ("Early detection", ["title screening in home repair programs", "title screening in tax credit or water discount applications", "senior service touchpoints", "property record and death record matching"]),
    ("Navigation and support", ["warm handoffs", "document collection help", "transportation support", "digital access assistance", "case tracking after referral"]),
    ("Legal resolution", ["probate assistance", "deed preparation", "legal aid", "mediation for family conflict", "tax sale prevention"]),
    ("Structural reform", ["stronger owner-occupied protections", "repair grant and title clearing integration", "better data sharing", "anti-speculation protections", "policy simplification"]),
]


THEME_BY_ID = {theme["id"]: theme for theme in INTERVIEW_THEMES}
NODE_BY_ID = {node["id"]: node for node in POWER_NODES}


def related_quotes_for_node(node_id: str, limit: int = 3) -> list[tuple[str, str]]:
    """Return selected quote snippets for themes related to a power-map node."""
    quotes: list[tuple[str, str]] = []
    for theme in INTERVIEW_THEMES:
        if node_id not in theme["related_power_nodes"]:
            continue
        for quote in theme["key_quotes"][:2]:
            quotes.append((theme["title"], quote))
            if len(quotes) >= limit:
                return quotes
    return quotes


def themes_for_node(node_id: str) -> list[dict]:
    return [theme for theme in INTERVIEW_THEMES if node_id in theme["related_power_nodes"]]


def nodes_for_theme(theme_id: str) -> list[dict]:
    theme = THEME_BY_ID.get(theme_id)
    if not theme:
        return []
    return [NODE_BY_ID[node_id] for node_id in theme["related_power_nodes"] if node_id in NODE_BY_ID]
