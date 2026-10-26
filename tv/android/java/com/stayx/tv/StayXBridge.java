// SPDX-License-Identifier: GPL-3.0-only
package com.stayx.tv;

import android.content.Context;
import android.content.Intent;
import android.content.ComponentName;
import android.net.Uri;
import android.os.Handler;
import android.os.Looper;
import android.widget.Toast;
import android.app.Activity;
import android.util.Log;
import java.io.InputStream;
import java.io.ByteArrayOutputStream;

/** Validated bridge from the TV player to the optional local download helper. */
public final class StayXBridge {
    private static final String HELPER = "com.deniscerri.ytdl";
    public static void attach(final Activity activity) {
        final Handler handler = new Handler(Looper.getMainLooper());
        handler.postDelayed(new Runnable() {
            private int remaining = 12;
            @Override public void run() {
                if (activity.isFinishing() || remaining-- <= 0) return;
                try {
                    InputStream stream = activity.getAssets().open("stayx-runtime.js");
                    ByteArrayOutputStream buffer = new ByteArrayOutputStream();
                    byte[] bytes = new byte[8192];
                    int count;
                    while ((count = stream.read(bytes)) != -1) buffer.write(bytes, 0, count);
                    stream.close();
                    String code = new String(buffer.toByteArray(), "UTF-8");
                    activity.getClass().getMethod("evaluateJavaScript", String.class).invoke(activity,
                        "if (window._yttv && !window.__stayxRuntimeLoaded) {" + code + "}");
                } catch (Exception error) { Log.w("StayXRuntime", "Runtime injection unavailable", error); }
                handler.postDelayed(this, 2500);
            }
        }, 1500);
    }
    public static boolean menuKey(Activity activity, int code) {
        if (code != 82) return false;
        try {
            activity.getClass().getMethod("evaluateJavaScript", String.class).invoke(activity,
                "console.info('StayX runtime ready: '+typeof window.stayxOpenSettings); window.stayxOpenSettings && window.stayxOpenSettings()");
            return true;
        } catch (Exception error) { return false; }
    }
    public static boolean handle(final Context context, String command) {
        if (command == null) return true;
        final Uri uri = Uri.parse(command);
        // This fork does not expose the upstream arbitrary APK installer to website scripts.
        if (!"stayx".equals(uri.getScheme())) return true;
        final String action = uri.getHost();
        if (!"download".equals(action) && !"downloads".equals(action)) return true;
        final String id = uri.getQueryParameter("videoId");
        if ("download".equals(action) && (id == null || !id.matches("[A-Za-z0-9_-]{11}"))) return true;
        new Handler(Looper.getMainLooper()).post(new Runnable() {
            @Override public void run() {
                try {
                    context.getPackageManager().getPackageInfo(HELPER, 0);
                    Intent intent;
                    if ("download".equals(action)) {
                        intent = new Intent(Intent.ACTION_SEND);
                        intent.setComponent(new ComponentName(HELPER, HELPER + ".receiver.ShareActivity"));
                        intent.setType("text/plain");
                        intent.putExtra(Intent.EXTRA_TEXT, "https://www.youtube.com/watch?v=" + id);
                        intent.putExtra("TYPE", "video");
                        intent.putExtra("quick_download", true);
                        intent.putExtra("BACKGROUND", true);
                    } else {
                        intent = new Intent(Intent.ACTION_VIEW);
                        intent.setComponent(new ComponentName(HELPER, HELPER + ".MainActivity"));
                        intent.putExtra("destination", "Downloads");
                    }
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    context.startActivity(intent);
                    if ("download".equals(action)) Toast.makeText(context, "Opening YTDLnis download queue", Toast.LENGTH_SHORT).show();
                } catch (Exception error) {
                    Toast.makeText(context, "Install and set up the YTDLnis helper to save videos locally.", Toast.LENGTH_LONG).show();
                }
            }
        });
        return true;
    }
}
