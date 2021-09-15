package com.example.iotssc;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.widget.TextView;

import com.google.android.material.floatingactionbutton.FloatingActionButton;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class RealTimeActivity extends AppCompatActivity {

    String result;
    TextView classification_result;
    Handler handler;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_realtime);

        classification_result = findViewById(R.id.textView2);
        ExecutorService executor = Executors.newSingleThreadExecutor();
        handler = new Handler(Looper.getMainLooper());

        executor.execute(new background_http());

        FloatingActionButton fab =  findViewById(R.id.realrefresh);
        fab.setOnClickListener(view -> executor.execute(new background_http()));
    }

    public class background_http implements Runnable {
        @Override
        public void run() {

            try{
                JSONObject jsonObject = getJSONObjectFromURL("https://iotssc-307717.uc.r.appspot.com/prediction/realtime/");
                result= jsonObject.getJSONObject("message").getString("classification");


            } catch (IOException e) {
                e.printStackTrace();
            } catch (JSONException e) {
                e.printStackTrace();
            }

            handler.post(() -> classification_result.setText(result));
        }
    }



    public static JSONObject getJSONObjectFromURL(String urlString) throws IOException, JSONException {
        HttpURLConnection urlConnection = null;
        URL url = new URL(urlString);
        urlConnection = (HttpURLConnection) url.openConnection();
        urlConnection.setRequestProperty("Authorization", "Token 0f6a47b2cd63013f5a8bcd221dd3efe4b9a65dbf");
        urlConnection.setRequestMethod("GET");
        urlConnection.setReadTimeout(10000 /* milliseconds */ );
        urlConnection.setConnectTimeout(15000 /* milliseconds */ );
//        urlConnection.setDoOutput(true);
        urlConnection.connect();

        System.out.println("code: " + urlConnection.getResponseCode());
        System.out.println("code: " + urlConnection.getResponseMessage());

        BufferedReader br = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
        StringBuilder sb = new StringBuilder();

        String line;
        while ((line = br.readLine()) != null) {
            sb.append(line + "\n");
        }
        br.close();

        String jsonString = sb.toString();
        System.out.println("JSON: " + jsonString);

        return new JSONObject(jsonString);
    }
}