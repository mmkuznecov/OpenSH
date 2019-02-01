package com.example.zinov.hackathonkek;

import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.TaskStackBuilder;
import android.content.Context;
import android.content.Intent;
import android.content.res.Resources;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Handler;
import android.os.StrictMode;
import android.support.v4.app.NotificationCompat;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.squareup.picasso.Picasso;

import org.apache.commons.net.ftp.FTPClient;
import org.apache.commons.net.ftp.FTPFile;

import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Arrays;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    private TextView mTv;
    private int mCounter;
    private int mMaxRepeat = 15;
    private Handler mHandler;
    private Runnable mRunnable;
    private int mInterval = 3000;
    private FTPClient ftpClient;
    private TextView ftpItemsOld;
    private TextView ftpItemsNew;
    public ImageView Face;
    private TextView tvDes;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        setContentView(R.layout.activity_main);
        // Get the application context
        StrictMode.setThreadPolicy(new StrictMode.ThreadPolicy.Builder()
                .detectDiskReads()
                .detectDiskWrites()
                .detectNetwork()   // or .detectAll() for all detectable problems
                .penaltyLog()
                .build());
        StrictMode.setVmPolicy(new StrictMode.VmPolicy.Builder()
                .detectLeakedSqlLiteObjects()
                .detectLeakedClosableObjects()
                .penaltyLog()
                .build());

        super.onCreate(savedInstanceState);
        ftpClient = new FTPClient();
        Face = (ImageView) findViewById(R.id.faceView);
        Face.setImageResource(R.drawable.misha);
        try {
            ftpClient.connect("rudy.zzz.com.ua");
            ftpClient.login("ondrey", "Freefree0");
            ftpClient.changeWorkingDirectory("ondrey.zzz.com.ua/peephole");
        } catch (IOException e) {
            e.printStackTrace();
        }

        Button btnStart = (Button) findViewById(R.id.btnStart);
        Button btnStop = (Button) findViewById(R.id.btnStop);

        mTv = (TextView) findViewById(R.id.tv);
        ftpItemsOld = (TextView) findViewById(R.id.ftpItemsOld);
        ftpItemsNew = (TextView) findViewById(R.id.ftpItemsNew);
        tvDes = (TextView) findViewById(R.id.textView3);
        mHandler = new Handler();

        btnStart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mHandler.removeCallbacks(mRunnable);
                mCounter = 0;
                mRunnable = new Runnable() {

                    @Override
                    public void run() {
                        doTask();
                    }
                };

                mHandler.postDelayed(mRunnable, (mInterval));
            }
        });
        btnStop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mHandler.removeCallbacks(mRunnable);
                mCounter = 0;
                mTv.setText(mCounter + " Dbg");
            }
        });
    }

    protected void doTask() {
        try {
            mCounter++;
            FTPFile[] nowFiles = ftpClient.listFiles();
            if (!(ftpItemsOld.getText().toString().equals(ftpItemsNew.getText().toString()))){
                Toast.makeText(this, "update", Toast.LENGTH_SHORT).show();

                List<String> linesOld = Arrays.asList(ftpItemsOld.getText().toString().split("\\r?\\n"));
                List<String> linesNew = Arrays.asList(ftpItemsNew.getText().toString().split("\\r?\\n"));
                for (String newLine: linesNew){
                    if (!linesOld.contains(newLine) && newLine.endsWith(".jpg")){
                        Face.setImageBitmap(getBitmapFromURL("http://topmegacool.ga/peephole/" + newLine));
                        tvDes.setText(newLine);
                        Toast.makeText(this, newLine, Toast.LENGTH_SHORT).show();
                    }
                }
            }

            ftpItemsOld.setText(ftpItemsNew.getText());
            ftpItemsNew.setText("");
            for (int i = 0; i < nowFiles.length; i++) {
                if (!nowFiles[i].getName().startsWith(".")) {
                    ftpItemsNew.setText(ftpItemsNew.getText() + nowFiles[i].getName() + "\n");
                }
            }
            mTv.setText(mCounter + " Dbg");
            mHandler.postDelayed(mRunnable, mInterval);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static Bitmap getBitmapFromURL(String src) {
        try {
            URL url = new URL(src);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoInput(true);
            connection.connect();
            InputStream input = connection.getInputStream();
            Bitmap myBitmap = BitmapFactory.decodeStream(input);
            return myBitmap;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
}