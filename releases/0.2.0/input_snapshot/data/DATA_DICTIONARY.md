# Knowledge-base data dictionary

Unknown values are `unavailable`. Foreign-key omissions are SQL NULL only when no record exists; they are not fabricated entity IDs. JSON arrays/objects inside CSV fields are serialized JSON. Numeric estimates are uncalibrated evidence summaries.

## entities

| Field | SQL definition |
|---|---|
| entity_id | entity_id TEXT PRIMARY KEY |
| name | name TEXT NOT NULL |
| entity_type | entity_type TEXT NOT NULL |
| layer | layer TEXT NOT NULL |
| external_id | external_id TEXT |
| species | species TEXT |
| mapping_status | mapping_status TEXT |

## entity_aliases

| Field | SQL definition |
|---|---|
| alias_id | alias_id TEXT PRIMARY KEY |
| entity_id | entity_id TEXT REFERENCES entities |
| original_label | original_label TEXT NOT NULL |
| assay_channel | assay_channel TEXT |
| resolution_status | resolution_status TEXT |
| source_id | source_id TEXT REFERENCES source_registry |

## entity_components

| Field | SQL definition |
|---|---|
| complex_id | complex_id TEXT REFERENCES entities |
| component_id | component_id TEXT REFERENCES entities |
| stoichiometry | stoichiometry TEXT |
| source_id | source_id TEXT REFERENCES source_registry |

## cells

| Field | SQL definition |
|---|---|
| cell_id | cell_id TEXT PRIMARY KEY |
| name | name TEXT NOT NULL |
| ontology_id | ontology_id TEXT |
| mapping_status | mapping_status TEXT |

## cell_states

| Field | SQL definition |
|---|---|
| state_id | state_id TEXT PRIMARY KEY |
| cell_id | cell_id TEXT REFERENCES cells |
| name | name TEXT |
| ontology_id | ontology_id TEXT |

## contexts

| Field | SQL definition |
|---|---|
| context_id | context_id TEXT PRIMARY KEY |
| species | species TEXT |
| ancestry | ancestry TEXT |
| age | age TEXT |
| sex | sex TEXT |
| tissue | tissue TEXT |
| disease | disease TEXT |
| disease_severity | disease_severity TEXT |
| treatment_status | treatment_status TEXT |
| cell_type | cell_type TEXT |
| cell_state | cell_state TEXT |
| developmental_state | developmental_state TEXT |
| stimulation | stimulation TEXT |
| dose | dose TEXT |
| duration | duration TEXT |
| assay | assay TEXT |
| genomic_background | genomic_background TEXT |
| time_point | time_point TEXT |

## cohorts

| Field | SQL definition |
|---|---|
| cohort_id | cohort_id TEXT PRIMARY KEY |
| dataset_id | dataset_id TEXT |
| accession | accession TEXT |
| study_id | study_id TEXT |
| participants | participants TEXT |
| ancestry | ancestry TEXT |
| species | species TEXT |
| tissue | tissue TEXT |
| cell_type | cell_type TEXT |
| disease | disease TEXT |
| intervention | intervention TEXT |
| sample_count | sample_count TEXT |
| donor_count | donor_count TEXT |
| parent_cohort | parent_cohort TEXT |
| related_publications | related_publications TEXT |
| independence_status | independence_status TEXT |
| notes | notes TEXT |

## datasets

| Field | SQL definition |
|---|---|
| dataset_id | dataset_id TEXT PRIMARY KEY |
| cohort_id | cohort_id TEXT REFERENCES cohorts |
| accession | accession TEXT |
| study_id | study_id TEXT |
| version | version TEXT |
| notes | notes TEXT |

## samples

| Field | SQL definition |
|---|---|
| sample_id | sample_id TEXT PRIMARY KEY |
| cohort_id | cohort_id TEXT REFERENCES cohorts |
| dataset_id | dataset_id TEXT REFERENCES datasets |
| donor_id | donor_id TEXT |
| context_id | context_id TEXT REFERENCES contexts |
| notes | notes TEXT |

## genetic_associations

| Field | SQL definition |
|---|---|
| record_id | record_id TEXT PRIMARY KEY |
| evidence_id | evidence_id TEXT REFERENCES evidence_instances |
| variant_entity_id | variant_entity_id TEXT REFERENCES entities |
| trait_entity_id | trait_entity_id TEXT REFERENCES entities |
| grade | grade TEXT |
| effect_size | effect_size TEXT |
| effect_unit | effect_unit TEXT |
| genome_build | genome_build TEXT |
| causal_gene_status | causal_gene_status TEXT |

## fine_mapping

| Field | SQL definition |
|---|---|
| record_id | record_id TEXT PRIMARY KEY |
| evidence_id | evidence_id TEXT REFERENCES evidence_instances |
| credible_set | credible_set TEXT |
| posterior_probability | posterior_probability TEXT |
| method | method TEXT |
| genome_build | genome_build TEXT |

## molecular_qtls

| Field | SQL definition |
|---|---|
| record_id | record_id TEXT PRIMARY KEY |
| evidence_id | evidence_id TEXT REFERENCES evidence_instances |
| qtl_type | qtl_type TEXT |
| target_entity_id | target_entity_id TEXT REFERENCES entities |
| effect_size | effect_size TEXT |
| effect_unit | effect_unit TEXT |
| colocalization | colocalization TEXT |

## regulatory_evidence

| Field | SQL definition |
|---|---|
| record_id | record_id TEXT PRIMARY KEY |
| evidence_id | evidence_id TEXT REFERENCES evidence_instances |
| regulatory_element_id | regulatory_element_id TEXT REFERENCES entities |
| perturbation | perturbation TEXT |
| measured_outcome | measured_outcome TEXT |

## transcriptomic_observations

| Field | SQL definition |
|---|---|
| record_id | record_id TEXT PRIMARY KEY |
| evidence_id | evidence_id TEXT REFERENCES evidence_instances |
| observation_type | observation_type TEXT |
| target_entity_id | target_entity_id TEXT REFERENCES entities |
| assay | assay TEXT |
| donor_model | donor_model TEXT |
| multiple_testing | multiple_testing TEXT |
| composition_qc | composition_qc TEXT |

## transcriptional_programs

| Field | SQL definition |
|---|---|
| program_id | program_id TEXT PRIMARY KEY |
| entity_id | entity_id TEXT REFERENCES entities |
| definition | definition TEXT |
| measured_or_inferred | measured_or_inferred TEXT |
| evidence_id | evidence_id TEXT REFERENCES evidence_instances |

## proteomic_observations

| Field | SQL definition |
|---|---|
| record_id | record_id TEXT PRIMARY KEY |
| evidence_id | evidence_id TEXT REFERENCES evidence_instances |
| target_entity_id | target_entity_id TEXT REFERENCES entities |
| measurement | measurement TEXT |
| platform | platform TEXT |
| biological_matrix | biological_matrix TEXT |
| reagent | reagent TEXT |
| isoform | isoform TEXT |
| limit_of_detection | limit_of_detection TEXT |
| normalization | normalization TEXT |
| peptide_uniqueness | peptide_uniqueness TEXT |
| localization | localization TEXT |
| cross_reactivity | cross_reactivity TEXT |

## protein_modifications

| Field | SQL definition |
|---|---|
| record_id | record_id TEXT PRIMARY KEY |
| evidence_id | evidence_id TEXT REFERENCES evidence_instances |
| protein_entity_id | protein_entity_id TEXT REFERENCES entities |
| modification | modification TEXT |
| site | site TEXT |
| measurement_method | measurement_method TEXT |

## edge_assertions

| Field | SQL definition |
|---|---|
| assertion_id | assertion_id TEXT PRIMARY KEY |
| subject_id | subject_id TEXT NOT NULL REFERENCES entities |
| predicate | predicate TEXT NOT NULL |
| object_id | object_id TEXT NOT NULL REFERENCES entities |
| context_id | context_id TEXT NOT NULL REFERENCES contexts |
| measurement | measurement TEXT NOT NULL |
| direction | direction TEXT NOT NULL |
| evidence_tier | evidence_tier TEXT |
| status | status TEXT |
| qualitative_confidence | qualitative_confidence TEXT |
| contradiction_group | contradiction_group TEXT |
| candidate_path | candidate_path TEXT |

## evidence_instances

| Field | SQL definition |
|---|---|
| evidence_id | evidence_id TEXT PRIMARY KEY |
| assertion_id | assertion_id TEXT NOT NULL REFERENCES edge_assertions |
| source_id | source_id TEXT NOT NULL REFERENCES source_registry |
| cohort_id | cohort_id TEXT NOT NULL REFERENCES cohorts |
| source_locator | source_locator TEXT NOT NULL |
| evidence_summary | evidence_summary TEXT NOT NULL |
| effect_size | effect_size TEXT |
| effect_unit | effect_unit TEXT |
| uncertainty | uncertainty TEXT |
| causal_directness | causal_directness TEXT |
| limitations | limitations TEXT |
| qc_status | qc_status TEXT |
| extraction_lane | extraction_lane TEXT |
| tested_hypothesis | tested_hypothesis TEXT |
| evidence_relation | evidence_relation TEXT |
| null_adequacy | null_adequacy TEXT |

## multiomic_links

| Field | SQL definition |
|---|---|
| link_id | link_id TEXT PRIMARY KEY |
| from_assertion_id | from_assertion_id TEXT REFERENCES edge_assertions |
| to_assertion_id | to_assertion_id TEXT REFERENCES edge_assertions |
| status | status TEXT |
| compatibility_report | compatibility_report TEXT |
| bridge_evidence_id | bridge_evidence_id TEXT REFERENCES evidence_instances |

## materialized_paths

| Field | SQL definition |
|---|---|
| path_id | path_id TEXT PRIMARY KEY |
| assertion_ids | assertion_ids TEXT |
| context_id | context_id TEXT REFERENCES contexts |
| compatibility_report | compatibility_report TEXT |
| status | status TEXT |

## prior_parameters

| Field | SQL definition |
|---|---|
| prior_id | prior_id TEXT PRIMARY KEY |
| assertion_id | assertion_id TEXT REFERENCES edge_assertions |
| parameter_family | parameter_family TEXT |
| distribution | distribution TEXT |
| parameters | parameters TEXT |
| estimate | estimate REAL |
| estimate_without_journal | estimate_without_journal REAL |
| independent_groups | independent_groups INTEGER |
| calibration_status | calibration_status TEXT |
| availability | availability TEXT |
| rationale | rationale TEXT |

## prior_changes

| Field | SQL definition |
|---|---|
| change_id | change_id TEXT PRIMARY KEY |
| prior_id | prior_id TEXT REFERENCES prior_parameters |
| previous_version | previous_version TEXT |
| new_version | new_version TEXT |
| previous_parameters | previous_parameters TEXT |
| new_parameters | new_parameters TEXT |
| reason | reason TEXT |

## critic_runs

| Field | SQL definition |
|---|---|
| critic_run_id | critic_run_id TEXT PRIMARY KEY |
| role | role TEXT |
| scope | scope TEXT |
| timestamp_start | timestamp_start TEXT |
| timestamp_end | timestamp_end TEXT |
| independence | independence TEXT |

## critic_findings

| Field | SQL definition |
|---|---|
| finding_id | finding_id TEXT PRIMARY KEY |
| critic_run_id | critic_run_id TEXT REFERENCES critic_runs |
| severity | severity TEXT |
| target_type | target_type TEXT |
| target_id | target_id TEXT |
| challenge | challenge TEXT |
| evidence | evidence TEXT |
| recommendation | recommendation TEXT |
| disposition | disposition TEXT |

## adjudications

| Field | SQL definition |
|---|---|
| adjudication_id | adjudication_id TEXT PRIMARY KEY |
| finding_id | finding_id TEXT REFERENCES critic_findings |
| adjudicator_role | adjudicator_role TEXT |
| decision | decision TEXT |
| rationale | rationale TEXT |
| human_adjudication_status | human_adjudication_status TEXT |

## journal_metrics

| Field | SQL definition |
|---|---|
| metric_id | metric_id TEXT PRIMARY KEY |
| journal | journal TEXT |
| year | year TEXT |
| impact_factor | impact_factor REAL |
| authoritative_source | authoritative_source TEXT |
| verified | verified INTEGER CHECK(verified IN (0,1)) |
| multiplier | multiplier REAL |

## source_registry

| Field | SQL definition |
|---|---|
| source_id | source_id TEXT PRIMARY KEY |
| title | title TEXT NOT NULL |
| authors | authors TEXT |
| year | year TEXT |
| url | url TEXT NOT NULL |
| doi | doi TEXT |
| pmid | pmid TEXT |
| source_type | source_type TEXT |
| version | version TEXT |
| retrieved_at | retrieved_at TEXT |
| access_level | access_level TEXT |
| snapshot_path | snapshot_path TEXT |
| snapshot_sha256 | snapshot_sha256 TEXT |
| species | species TEXT |
| notes | notes TEXT |
| ingestion_status | ingestion_status TEXT |
| duplicate_of | duplicate_of TEXT |

## search_log

| Field | SQL definition |
|---|---|
| search_id | search_id TEXT PRIMARY KEY |
| lane | lane TEXT |
| query | query TEXT |
| database | database TEXT |
| searched_at | searched_at TEXT |
| result_source_ids | result_source_ids TEXT |
| screening_notes | screening_notes TEXT |
| snapshot_path | snapshot_path TEXT |
| total_hits | total_hits TEXT |
| returned_pmids | returned_pmids TEXT |
| retrieval_limit | retrieval_limit TEXT |

## screening_decisions

| Field | SQL definition |
|---|---|
| screening_id | screening_id TEXT PRIMARY KEY |
| source_id | source_id TEXT REFERENCES source_registry |
| decision | decision TEXT |
| reason | reason TEXT |
| stage | stage TEXT |
| reviewer_role | reviewer_role TEXT |

## agent_runs

| Field | SQL definition |
|---|---|
| run_id | run_id TEXT PRIMARY KEY |
| agent_role | agent_role TEXT |
| timestamp_start | timestamp_start TEXT |
| timestamp_end | timestamp_end TEXT |
| timezone | timezone TEXT |
| LLM_provider | LLM_provider TEXT |
| LLM_model | LLM_model TEXT |
| model_snapshot_if_available | model_snapshot_if_available TEXT |
| reasoning_mode | reasoning_mode TEXT |
| protocol_version | protocol_version TEXT |
| agent_prompt_version | agent_prompt_version TEXT |
| instruction_bundle_hash | instruction_bundle_hash TEXT |
| source_versions | source_versions TEXT |
| retrieval_queries | retrieval_queries TEXT |
| retrieval_dates | retrieval_dates TEXT |
| source_hashes | source_hashes TEXT |
| code_commit | code_commit TEXT |
| environment_hash | environment_hash TEXT |
| output_hash | output_hash TEXT |
| critic_run_ids | critic_run_ids TEXT |
| human_edits | human_edits TEXT |
| original_metadata | original_metadata TEXT |

## instruction_versions

| Field | SQL definition |
|---|---|
| instruction_id | instruction_id TEXT PRIMARY KEY |
| version | version TEXT |
| path | path TEXT |
| sha256 | sha256 TEXT |
| scope | scope TEXT |

## artifact_hashes

| Field | SQL definition |
|---|---|
| artifact_id | artifact_id TEXT PRIMARY KEY |
| path | path TEXT NOT NULL |
| sha256 | sha256 TEXT NOT NULL |
| hash_scope | hash_scope TEXT |

## coverage_gaps

| Field | SQL definition |
|---|---|
| gap_id | gap_id TEXT PRIMARY KEY |
| lane | lane TEXT |
| description | description TEXT |
| status | status TEXT |

## assay_coverage

| Field | SQL definition |
|---|---|
| original_label | original_label TEXT PRIMARY KEY |
| entity_id | entity_id TEXT REFERENCES entities |
| mapping_status | mapping_status TEXT |
| related_assertion_count | related_assertion_count INTEGER |
| reviewed_protein_assertion_count | reviewed_protein_assertion_count INTEGER |
| coverage_status | coverage_status TEXT |

## screening_candidates

| Field | SQL definition |
|---|---|
| candidate_id | candidate_id TEXT PRIMARY KEY |
| query_id | query_id TEXT |
| title | title TEXT |
| url | url TEXT |
| doi | doi TEXT |
| pmid | pmid TEXT |
| decision | decision TEXT |
| reason | reason TEXT |
| lane | lane TEXT |

## quantitative_results

| Field | SQL definition |
|---|---|
| result_id | result_id TEXT PRIMARY KEY |
| evidence_id | evidence_id TEXT REFERENCES evidence_instances |
| reported_result | reported_result TEXT |
| interpretation | interpretation TEXT |

## release_changes

| Field | SQL definition |
|---|---|
| change_id | change_id TEXT PRIMARY KEY |
| record_type | record_type TEXT |
| record_id | record_id TEXT |
| previous_version | previous_version TEXT |
| new_version | new_version TEXT |
| change_type | change_type TEXT |
| old_record | old_record TEXT |
| new_record | new_record TEXT |

