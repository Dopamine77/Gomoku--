#include "mongoose.h"
#include <string>
using namespace std;

static int exit_flag = 0;
static string msg;

static void ev_handler(struct mg_connection *c, int ev, void *p) {
  if (ev == MG_EV_HTTP_REPLY) {
    struct http_message *hm = (struct http_message *)p;
    c->flags |= MG_F_CLOSE_IMMEDIATELY;
    msg = hm->body.p;
    // fwrite(hm->message.p, 1, (int)hm->message.len, stdout);
    // putchar('\n');
    exit_flag = 1;
  } else if (ev == MG_EV_CLOSE) {
    exit_flag = 1;
  };
}

string http_get(string url){
  exit_flag = 0;
  
  struct mg_mgr mgr;
  mg_mgr_init(&mgr, NULL);
  mg_connect_http(&mgr, ev_handler, url.c_str(), NULL, NULL);

  while (exit_flag == 0) {
    mg_mgr_poll(&mgr, 1000);
  }
  mg_mgr_free(&mgr);
  if(exit_flag == 1){
    return msg;
  }
  return "error";
}

// int main() {
//   cout << http_get("http://202.207.12.223:8000/context/86e0caa3527526e88c3300ff4c2c3d6e");
// }

