#pragma once

struct DDS_info {
	string file;
	int org_len;
	int len;
	void *org_buff;
	void *buff;
};

const vector<pair<DDS_info, DDS_info>> *af_get_replace_vector();
