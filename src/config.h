#ifndef UZBL_CONFIG_H
#define UZBL_CONFIG_H

#include <glib.h>

const gchar * const
default_config[] = {
"set status_format <b>\\@[\\@TITLE]\\@</b> - \\@[\\@uri]\\@ - <span foreground=\"#bbb\">\\@NAME</span>",
"set show_status 1",
"set title_format_long \\@keycmd \\@TITLE - Uzbl browser <\\@NAME> > \\@SELECTED_URI",
"set title_format_short \\@TITLE - Uzbl browser <\\@NAME>",
"set max_conns 100", /* WebKitGTK default: 10 */
"set max_conns_host 6", /* WebKitGTK default: 2 */
"set shell_cmd /bin/sh -c",
"set maintain_history 1", /* Set here since the WebKit default is 1, but there's no way to get the current value. */
"set forward_keys 1", /* Forward keys by default so that webpages work as expected without a config. */
"set zoom_text_only 0", /* Zoom all content by default; text-only is not as useful. */
NULL
};

#endif
