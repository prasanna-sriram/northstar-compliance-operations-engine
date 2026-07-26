USE NorthStarDigitalBank
GO

----DROP TABLE IF EXISTS controls
--CREATE TABLE controls
--(
--	control_id VARCHAR(20) PRIMARY KEY NOT NULL,
--	framework VARCHAR(50) NOT NULL,
--	domain VARCHAR(100) NOT NULL,
--	control_name VARCHAR(250) NOT NULL,
--	owner VARCHAR(50) NOT NULL,
--	test_frequency VARCHAR(50) NOT NULL,
--	evidence_required VARCHAR(100) NOT NULL,
--	status VARCHAR(50) NOT NULL
--)


--DROP TABLE IF EXISTS framework_mapping
--CREATE TABLE framework_mapping
--(
--	control_id VARCHAR(20) PRIMARY KEY NOT NULL,
--	iso_clause VARCHAR(50) NOT NULL,
--	iso_annex_a_control VARCHAR(250) NOT NULL,
--	soc2_tsc VARCHAR(100) NOT NULL,
--	nist_csf_function VARCHAR(50) NOT NULL,
--	control_objective VARCHAR(250) NOT NULL
--)


----DROP TABLE IF EXISTS control_tests
--CREATE TABLE control_tests
--(
--	test_id VARCHAR(20) PRIMARY KEY NOT NULL,
--	control_id VARCHAR(20) NOT NULL,
--	test_date DATE NOT NULL,
--	tester VARCHAR(50) NOT NULL,
--	result VARCHAR(100) NOT NULL,
--	issues_found VARCHAR(250) NOT NULL
--	CONSTRAINT FK_ct_c FOREIGN KEY (control_id) REFERENCES controls(control_id)
--)

----DROP TABLE IF EXISTS evidence_inventory
--CREATE TABLE evidence_inventory
--(
--	evidence_id VARCHAR(20) PRIMARY KEY NOT NULL,
--	control_id VARCHAR(20) NOT NULL,
--	evidence_name VARCHAR(250) NOT NULL,
--	source_system VARCHAR(100) NOT NULL,
--	owner VARCHAR(50) NOT NULL,
--	last_collected_date DATE NOT NULL,
--	next_due_date DATE NOT NULL,
--	status VARCHAR(50) NOT NULL,
--	CONSTRAINT FK_ei_c FOREIGN KEY (control_id) REFERENCES controls(control_id)
--)


----DROP TABLE IF EXISTS policy_register
--CREATE TABLE policy_register
--(
--	policy_id VARCHAR(20) PRIMARY KEY NOT NULL,
--	policy_name VARCHAR(250) NOT NULL,
--	owner VARCHAR(50) NOT NULL,
--	version VARCHAR(20) NOT NULL,
--	last_review_date DATE NOT NULL,
--	next_review_date DATE NOT NULL,
--	attestation_required VARCHAR(20) NOT NULL,
--	status VARCHAR(50) NOT NULL
--)


----DROP TABLE IF EXISTS risk_register
--CREATE TABLE risk_register
--(
--	risk_id VARCHAR(20) PRIMARY KEY NOT NULL,
--	risk_title VARCHAR(100) NOT NULL,
--	category VARCHAR(50) NOT NULL,
--	likelihood INT NOT NULL,
--	impact INT NOT NULL,
--	inherent_score INT NOT NULL,
--	control_strength VARCHAR(20) NOT NULL,
--	residual_score INT NOT NULL,
--	treatment_plan VARCHAR(250) NOT NULL,
--	owner VARCHAR(50) NOT NULL,
--	target_date DATE NOT NULL,
--	status VARCHAR(20) NOT NULL
--)


----DROP TABLE IF EXISTS corrective_actions
--CREATE TABLE corrective_actions
--(
--	ca_id VARCHAR(20) PRIMARY KEY NOT NULL,
--	source VARCHAR(50) NOT NULL,
--	related_item VARCHAR(100) NOT NULL,
--	root_cause VARCHAR(250) NOT NULL,
--	owner VARCHAR(50) NOT NULL,
--	opened_date DATE NOT NULL,
--	target_date DATE NOT NULL,
--	status VARCHAR(20) NOT NULL,
--	effectiveness_review VARCHAR(250) NOT NULL
--)


----DROP TABLE IF EXISTS vendors
--CREATE TABLE vendors
--(
--	vendor_id VARCHAR(20) PRIMARY KEY NOT NULL,
--	vendor_name VARCHAR(50) NOT NULL,
--	service_type VARCHAR(50) NOT NULL,
--	data_sensitivity VARCHAR(20) NOT NULL,
--	connectivity VARCHAR(20) NOT NULL,
--	criticality VARCHAR(20) NOT NULL,
--	privileged_access VARCHAR(10) NOT NULL,
--	risk_tier VARCHAR(20) NOT NULL
--)


----DROP TABLE IF EXISTS vendor_assessment
--CREATE TABLE vendor_assessment
--(
--	assessment_id VARCHAR(20) PRIMARY KEY NOT NULL,
--	vendor_id VARCHAR(20) NOT NULL,
--	assessment_date DATE NOT NULL,
--	review_type VARCHAR(50) NOT NULL,
--	security_score INT NOT NULL,
--	open_findings INT NOT NULL,
--	next_review_due DATE NOT NULL,
--	CONSTRAINT FK_va_v FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
--)


----DROP TABLE IF EXISTS privacy_requests
--CREATE TABLE privacy_requests
--(
--	request_id VARCHAR(20) PRIMARY KEY NOT NULL,
--	request_type VARCHAR(50) NOT NULL,
--	received_date DATE NOT NULL,
--	due_date DATE NOT NULL,
--	status VARCHAR(20) NOT NULL,
--	days_open INT NOT NULL,
--	owner VARCHAR(50) NOT NULL
--)


----DROP TABLE IF EXISTS data_inventory
--CREATE TABLE data_inventory
--(
--	asset_id VARCHAR(20) PRIMARY KEY NOT NULL,
--	system_name VARCHAR(50) NOT NULL,
--	data_type VARCHAR(250) NOT NULL,
--	contains_pii VARCHAR(20) NOT NULL,
--	residency VARCHAR(100) NOT NULL,
--	retention_period VARCHAR(100) NOT NULL,
--	lawful_purpose VARCHAR(250) NOT NULL,
--	owner VARCHAR(50) NOT NULL
--)