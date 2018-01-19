#include <sstream>

#include "../api/replay/renderdoc_replay.h"

#include "af.h"

#define DDS_HEADER_LEN (128)

#define ASSERT(X) \
do { \
	if (!(X)) { \
		fprintf(stderr, "[AF] ASSERT failed: " #X ", line %d\n", __LINE__); \
		abort(); \
	} \
} while(0)

static char gs_szIniFile[1024] = {0};

static int gs_iReplaceNum = 0;

static map<string, DDS_info> gs_mDDSs;
static vector<pair<DDS_info, DDS_info>> gs_vecReplace;

DDS_info add_new_dds(const char *filename) {
	string fn(filename);
	if (0 == gs_mDDSs.count(fn)) {
		//FILE *fp = fopen(fn.c_str(), "rb");
		FILE *fp = NULL;
		fopen_s(&fp, fn.c_str(), "rb");
		ASSERT(fp != NULL);
		fseek(fp, 0, SEEK_END);
		int len = ftell(fp);
		fseek(fp, 0, SEEK_SET);
		char *buff = new char[len];
		ASSERT(1 == fread(buff, len, 1, fp));
		fclose(fp);

		DDS_info info;
		info.file = fn;
		info.org_len = len;
		info.org_buff = buff;
		info.len = len - DDS_HEADER_LEN;
		ASSERT(info.len > 0);
		info.buff = buff + DDS_HEADER_LEN;

		gs_mDDSs.insert(pair<string, DDS_info>(fn, info));
	}
	return gs_mDDSs.at(fn);
}

static int init() {
	printf("init: %s\n", gs_szIniFile);
	gs_iReplaceNum = GetPrivateProfileIntA("replace", "num", 0, gs_szIniFile);
	printf("replace.num = %d\n", gs_iReplaceNum);
	for (int i = 0; i < gs_iReplaceNum; i++) {
		std::stringstream skey;
		skey << "src_dds_" << (i+1);
		std::stringstream dkey;
		dkey << "dst_dds_" << (i+1);
		char src[256];
		char dst[256];
		GetPrivateProfileStringA("replace", skey.str().c_str(), "", src, sizeof(src), gs_szIniFile);
		GetPrivateProfileStringA("replace", dkey.str().c_str(), "", dst, sizeof(dst), gs_szIniFile);
		printf("  %s -> %s\n", src, dst);
		ASSERT(src[0] != 0);
		ASSERT(dst[0] != 0);
		DDS_info a = add_new_dds(src);
		DDS_info b = add_new_dds(dst);
		gs_vecReplace.push_back(pair<DDS_info, DDS_info>(a, b));
	}
	return 0;
}

const vector<pair<DDS_info, DDS_info>> *af_get_replace_vector() {
	return &gs_vecReplace;
}

extern "C" RENDERDOC_API int af_init_by_config(const char *filename) {
	strcpy_s(gs_szIniFile, filename);
	return init();
}
