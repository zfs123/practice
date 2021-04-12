/**
 *
 * A practice module for Nginx.
 *
 */

#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>


typedef struct {
	ngx_flag_t  on;
} ngx_http_hello_loc_conf_t;

static void *ngx_http_hello_create_loc_conf(ngx_conf_t *cf);
static char *ngx_http_hello_merge_loc_conf(ngx_conf_t *cf, void *parent, void *child);
static char *ngx_http_hello(ngx_conf_t *cf);
static ngx_int_t ngx_http_hello_handler(ngx_http_request_t *r);

/* This module provided directive: hello on/off; */
static ngx_command_t ngx_http_hello_commands[] = {
    { ngx_string("hello"),
	  NGX_HTTP_LOC_CONF|NGX_CONF_TAKE1,
	  ngx_conf_set_flag_slot,
	  NGX_HTTP_LOC_CONF_OFFSET,
	  offsetof(ngx_http_hello_loc_conf_t, on),
	  NULL },

    ngx_null_command /* command termination */
};

/* The hello world string. */
static u_char ngx_hello_str[] = "hello\r\n";

/* The module context. */
static ngx_http_module_t ngx_http_hello_module_ctx = {
    NULL, /* preconfiguration */
    ngx_http_hello, /* postconfiguration */

    NULL, /* create main configuration */
    NULL, /* init main configuration */

    NULL, /* create server configuration */
    NULL, /* merge server configuration */

    ngx_http_hello_create_loc_conf,          /* create location configuration */
    NULL           /* merge location configuration */
};

static void *
ngx_http_hello_create_loc_conf(ngx_conf_t *cf)
{
	ngx_http_hello_loc_conf_t *conf;
	conf = ngx_pcalloc(cf->pool, sizeof(ngx_http_hello_loc_conf_t));
    if (conf == NULL) {
        return NULL;
    }
	conf->on = NGX_CONF_UNSET;
	return conf;
}

/* Module definition. */
ngx_module_t ngx_http_hello_module = {
    NGX_MODULE_V1,
    &ngx_http_hello_module_ctx, /* module context */
    ngx_http_hello_commands, /* module directives */
    NGX_HTTP_MODULE, /* module type */
    NULL, /* init master */
    NULL, /* init module */
    NULL, /* init process */
    NULL, /* init thread */
    NULL, /* exit thread */
    NULL, /* exit process */
    NULL, /* exit master */
    NGX_MODULE_V1_PADDING
};

/**
 * Content handler.
 *
 * @param r
 *   Pointer to the request structure. See http_request.h.
 * @return
 *   The status of the response generation.
 */
static ngx_int_t ngx_http_hello_handler(ngx_http_request_t *r)
{
    ngx_buf_t *b;
    ngx_chain_t out;

    /* Set the Content-Type header. */
    r->headers_out.content_type.len = sizeof("text/plain") - 1;
    r->headers_out.content_type.data = (u_char *) "text/plain";

    /* Allocate a new buffer for sending out the reply. */
    b = ngx_pcalloc(r->pool, sizeof(ngx_buf_t));

    /* Insertion in the buffer chain. */
    out.buf = b;
    out.next = NULL; /* just one buffer */

    b->pos = ngx_hello_str; /* first position in memory of the data */
    b->last = ngx_hello_str + sizeof(ngx_hello_str) - 1; /* last position in memory of the data */
    b->memory = 1; /* content is in read-only memory */
    b->last_buf = 1; /* there will be no more buffers in the request */

    /* Sending the headers for the reply. */
    r->headers_out.status = NGX_HTTP_OK; /* 200 status code */
    /* Get the content length of the body. */
    r->headers_out.content_length_n = sizeof(ngx_hello_str) - 1;
    ngx_http_send_header(r); /* Send the headers */

    /* Send the body, and return the status code of the output filter chain. */
    return ngx_http_output_filter(r, &out);
} /* ngx_http_hello_handler */

/**
 * Configuration setup function that installs the content handler.
 *
 * @param cf
 *   Module configuration structure pointer.
 * @return string
 *   Status of the configuration setup.
 */
static char *ngx_http_hello(ngx_conf_t *cf)
{
    ngx_http_core_loc_conf_t *clcf; /* pointer to core location configuration */

    /* Install the hello world handler. */
    clcf = ngx_http_conf_get_module_loc_conf(cf, ngx_http_core_module);
    clcf->handler = ngx_http_hello_handler;

    return NGX_CONF_OK;
} /* ngx_http_hello */