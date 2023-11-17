package com.example.mqtt;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.SwitchCompat;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.TextView;
import android.widget.Toast;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttMessage;


public class MainActivity extends AppCompatActivity {
    MQTTHelper mqttHelper;
    TextView txtNhietDo, txtDoam, txtGas, txtThongBao;
    SwitchCompat swOnOff;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        txtNhietDo = findViewById(R.id.txtNhietDo);
        txtDoam = findViewById(R.id.txtDoAm);
        txtGas = findViewById(R.id.txtKhiGas);
        txtThongBao = findViewById(R.id.txtThongBao);
        swOnOff = findViewById(R.id.swOnOff);
        startMQTT();

    }

    public void startMQTT() {
        mqttHelper = new MQTTHelper(this);
//        btnDark.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                mqttHelper.publishToTopic("diemcongbinh/feeds/bong-den", "0");
//            }
//        });
        mqttHelper.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {

            }

            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Log.d("TEST", topic + "***" + message.toString());
                swOnOff.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                    @Override
                    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                        String message;
                        if (isChecked) {
                            message = "1"; // ON
                        } else {
                            message = "0"; // OFF
                        }

                        mqttHelper.publishToTopic("diemcongbinh/feeds/bong-den", message);
                    }
                });


                if (topic.equals("diemcongbinh/feeds/nhiet-do")) {
                    float nhietDoValue = Float.parseFloat(message.toString());
                    txtNhietDo.setText("T: " + nhietDoValue + "°C");
                    if (nhietDoValue < 20 || nhietDoValue > 50) {
                        txtNhietDo.setBackgroundColor(getResources().getColor(R.color.warning));
                        txtDoam.setBackgroundColor(getResources().getColor(R.color.warning));
                        String msg = "Cảnh báo nhiệt độ, nhiệt độ hiện tại " + nhietDoValue;
                        //Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show();
                        AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                        builder.setTitle("Temperature Alert")
                                .setMessage(msg)
                                .setPositiveButton("OK", null)
                                .show();
                    } else
                        txtNhietDo.setBackgroundColor(getResources().getColor(R.color.normal));
                } else if (topic.equals("diemcongbinh/feeds/do-am")) {
                    float doAmValue = Float.parseFloat(message.toString());
                    txtDoam.setText("H: " + doAmValue + "%");
                    if (doAmValue > 90) {
                        txtDoam.setBackgroundColor(getResources().getColor(R.color.warning));
                        String msg = "Cảnh báo độ ẩm, độ ẩm hiện tại " + doAmValue;
                        //Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show();
                        AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                        builder.setTitle("Humidity Alert")
                                .setMessage(msg)
                                .setPositiveButton("OK", null)
                                .show();
                    } else
                        txtDoam.setBackgroundColor(getResources().getColor(R.color.normal));
                } else if (topic.equals("diemcongbinh/feeds/khi-gas")) {
                    int khiGasValue = Integer.parseInt(message.toString());

                    txtGas.setText("G: " + khiGasValue + "ppb");

                    if (khiGasValue > 512) {
                        txtGas.setBackgroundColor(getResources().getColor(R.color.warning));
                        String msg = "Cảnh báo khí Gas, khí gas hiện tại " + khiGasValue;
                        //Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show();
                        AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                        builder.setTitle("Gas Alert")
                                .setMessage(msg)
                                .setPositiveButton("OK", null)
                                .show();
                    } else
                        txtGas.setBackgroundColor(getResources().getColor(R.color.normal));
                }else if (topic.equals("diemcongbinh/feeds/bong-den")) {
                    String buttonState = message.toString();
                    if ("0".equals(buttonState)) {
                        // OFF
                        swOnOff.setChecked(false);

                    } else if ("1".equals(buttonState)) {
                        // ON
                        swOnOff.setChecked(true);
                    }
                }

                swOnOff.setOnCheckedChangeListener((buttonView, isChecked) -> {
                    String msg = isChecked ? "1" : "0";
                    mqttHelper.publishToTopic("diemcongbinh/feeds/bong-den", msg);
                });


            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }


}