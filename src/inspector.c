#include "inspector.h"

#include "events.h"
#include "type.h"
#include "util.h"
#include "uzbl-core.h"

struct _UzblInspector {
    GtkWidget *window;
};

/* =========================== PUBLIC API =========================== */

static WebKitWebView *
inspector_create_cb (WebKitWebInspector *inspector, WebKitWebView *view, gpointer data);
static gboolean
inspector_show_window_cb (WebKitWebInspector *inspector, gpointer data);
static gboolean
inspector_close_window_cb (WebKitWebInspector *inspector, gpointer data);
static gboolean
inspector_attach_window_cb (WebKitWebInspector *inspector, gpointer data);
static gboolean
inspector_detach_window_cb (WebKitWebInspector *inspector, gpointer data);
static gboolean
inspector_inspector_destroyed_cb (WebKitWebInspector *inspector, gpointer data);
static gboolean
inspector_uri_changed_cb (WebKitWebInspector *inspector, gpointer data);

void
uzbl_inspector_init ()
{
    uzbl.inspector = g_malloc0 (sizeof (UzblInspector));

    WebKitWebSettings *settings = webkit_web_view_get_settings (uzbl.gui.web_view);
    g_object_set (G_OBJECT (settings),
        "enable-developer-extras", TRUE,
        NULL);

    uzbl.gui.inspector = webkit_web_view_get_inspector (uzbl.gui.web_view);

    g_object_connect (G_OBJECT (uzbl.gui.inspector),
        "signal::inspect-web-view",      G_CALLBACK (inspector_create_cb),              NULL,
        "signal::show-window",           G_CALLBACK (inspector_show_window_cb),         NULL,
        "signal::close-window",
                                         G_CALLBACK (inspector_close_window_cb),        NULL,
        "signal::attach-window",
                                         G_CALLBACK (inspector_attach_window_cb),       NULL,
        "signal::detach-window",
                                         G_CALLBACK (inspector_detach_window_cb),       NULL,
        "signal::finished",              G_CALLBACK (inspector_inspector_destroyed_cb), NULL,
        "signal::notify::inspected-uri", G_CALLBACK (inspector_uri_changed_cb),         NULL,
        NULL);
}

void
uzbl_inspector_free ()
{
    g_free (uzbl.inspector);
    uzbl.inspector = NULL;
}

/* ==================== CALLBACK IMPLEMENTATIONS ==================== */

static void
inspector_hide_window_cb (GtkWidget *widget, gpointer data);

WebKitWebView *
inspector_create_cb (WebKitWebInspector *inspector, WebKitWebView *view, gpointer data)
{
    UZBL_UNUSED (inspector);
    UZBL_UNUSED (view);
    UZBL_UNUSED (data);

    GtkWidget *scrolled_window;
    GtkWidget *new_web_view;

    uzbl.inspector->window = gtk_window_new (GTK_WINDOW_TOPLEVEL);

    g_object_connect (G_OBJECT (uzbl.inspector->window),
        "signal::delete-event", G_CALLBACK (inspector_hide_window_cb), NULL,
        NULL);

    gtk_window_set_title (GTK_WINDOW (uzbl.inspector->window), "Uzbl WebInspector");
    gtk_window_set_default_size (GTK_WINDOW (uzbl.inspector->window), 400, 300);
    gtk_widget_show (uzbl.inspector->window);

    scrolled_window = gtk_scrolled_window_new (NULL, NULL);
    gtk_scrolled_window_set_policy (GTK_SCROLLED_WINDOW (scrolled_window),
        GTK_POLICY_AUTOMATIC, GTK_POLICY_AUTOMATIC);
    gtk_container_add (GTK_CONTAINER (uzbl.inspector->window), scrolled_window);
    gtk_widget_show (scrolled_window);

    new_web_view = webkit_web_view_new ();
    gtk_container_add (GTK_CONTAINER (scrolled_window), new_web_view);

    return WEBKIT_WEB_VIEW (new_web_view);
}

gboolean
inspector_show_window_cb (WebKitWebInspector *inspector, gpointer data)
{
    UZBL_UNUSED (inspector);
    UZBL_UNUSED (data);

    gtk_widget_show (uzbl.inspector->window);

    uzbl_events_send (WEBINSPECTOR, NULL,
        TYPE_NAME, "open",
        NULL);

    return TRUE;
}

gboolean
inspector_close_window_cb (WebKitWebInspector *inspector, gpointer data)
{
    UZBL_UNUSED (inspector);
    UZBL_UNUSED (data);

    gtk_widget_hide (uzbl.inspector->window);

    uzbl_events_send (WEBINSPECTOR, NULL,
        TYPE_NAME, "close",
        NULL);

    return TRUE;
}

/* TODO: Add variables and code to make use of these functions. */
gboolean
inspector_attach_window_cb (WebKitWebInspector *inspector, gpointer data)
{
    UZBL_UNUSED (inspector);
    UZBL_UNUSED (data);

    return FALSE;
}

gboolean
inspector_detach_window_cb (WebKitWebInspector *inspector, gpointer data)
{
    UZBL_UNUSED (inspector);
    UZBL_UNUSED (data);

    return FALSE;
}

gboolean
inspector_inspector_destroyed_cb (WebKitWebInspector *inspector, gpointer data)
{
    UZBL_UNUSED (inspector);
    UZBL_UNUSED (data);

    return FALSE;
}

gboolean
inspector_uri_changed_cb (WebKitWebInspector *inspector, gpointer data)
{
    UZBL_UNUSED (inspector);
    UZBL_UNUSED (data);

    return FALSE;
}

void
inspector_hide_window_cb (GtkWidget *widget, gpointer data)
{
    UZBL_UNUSED (data);

    gtk_widget_hide (widget);
}
