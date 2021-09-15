package com.example.iotssc;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;

import com.google.android.material.floatingactionbutton.FloatingActionButton;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class HistoricalActivity extends AppCompatActivity {

    private static final String TAG = "";
    private RecyclerView mRecyclerView;
    private List<Object> viewItems = new ArrayList<>();
    private RecyclerView.Adapter mAdapter;
    private RecyclerView.LayoutManager layoutManager;
    Handler handler;
    JSONObject jsonObject;
    JSONArray jsonArray;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_historical);
        mRecyclerView = findViewById(R.id.historyView);

        mRecyclerView.setHasFixedSize(true);

        layoutManager = new LinearLayoutManager(this);
        mRecyclerView.setLayoutManager(layoutManager);

        mAdapter = new RecyclerAdapter(this, viewItems);
        mRecyclerView.setAdapter(mAdapter);

        ExecutorService executor = Executors.newSingleThreadExecutor();
        handler = new Handler(Looper.getMainLooper());

        executor.execute(new background_http());

        FloatingActionButton fab =  findViewById(R.id.historyrefresh);
        fab.setOnClickListener(view -> executor.execute(new background_http()));

    }


    public class background_http implements Runnable {
        @Override
        public void run() {
            try {

                jsonObject = getJSONObjectFromURL("https://iotssc-307717.uc.r.appspot.com/prediction/historical/");
                jsonArray = jsonObject.getJSONArray("message");

            } catch (JSONException | IOException e) {
                Log.d(TAG, "addItemsFromJSON: ", e);
            }

            handler.post(() -> {
                System.out.println("123"+ jsonArray);
                try {
                    for (int i=0; i<jsonArray.length(); ++i) {
                        JSONObject itemObj = jsonArray.getJSONObject(i);

                        String time = itemObj.getString("timestamp");
                        String class_result = itemObj.getString("classification");
                        SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd HH-mm-ss-SSSSSS");

                        Date date = fmt.parse(time);
                        SimpleDateFormat fmtOut = new SimpleDateFormat("HH:mm:ss dd/MM/yyyy");
                        String resultDate = fmtOut.format(date);

                        Result results = new Result(resultDate,class_result);
                        viewItems.add(results);
                    }

                }catch (Exception e){
                    e.printStackTrace();
                }

                mAdapter.notifyDataSetChanged();
            });
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