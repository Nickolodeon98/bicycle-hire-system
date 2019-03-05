package com.example.bottomnav.internet;

import android.util.Log;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * @author Administrator
 * @version $Rev$
 * @des ${TODO}
 * @updateAuthor $Author$
 * @updateDes ${TODO}
 */
public class internet {
    public static String gethttpresult(String urlStr){
        try {
            URL url=new URL(urlStr);
            HttpURLConnection connect=(HttpURLConnection)url.openConnection();
            InputStream input=connect.getInputStream();
            BufferedReader in = new BufferedReader(new InputStreamReader(input));
            String line = null;
            System.out.println(connect.getResponseCode());
            StringBuffer sb = new StringBuffer();
            while ((line = in.readLine()) != null) {
                sb.append(line);
            }
            return sb.toString();
        } catch (Exception e) {
            System.out.println(e.toString());
            return null;
        }
    }
    public static String gethttppostresult(String urlStr,int id){
        String params = "{\"article_id\":1,\"user_id\":2}";
        try {
            URL url=new URL(urlStr);
            HttpURLConnection connect=(HttpURLConnection)url.openConnection();
            connect.setDoInput(true);
            connect.setDoOutput(true);
            connect.setRequestMethod("POST");
            connect.setUseCaches(false);
            connect.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            OutputStream outputStream = connect.getOutputStream();
            outputStream.write(params.getBytes());
            int response = connect.getResponseCode();
            if (response== HttpURLConnection.HTTP_OK)
            {
                System.out.println(response);
                InputStream input=connect.getInputStream();
                BufferedReader in = new BufferedReader(new InputStreamReader(input));
                String line = null;
                System.out.println(connect.getResponseCode());
                StringBuffer sb = new StringBuffer();
                while ((line = in.readLine()) != null) {
                    sb.append(line);
                }
                return sb.toString();
            }
            else {
                System.out.println(response);
                return "not exsits";
            }
        } catch (Exception e) {
            Log.e("e:", String.valueOf(e));
            return "internet errar";
        }
    }

    /**
     * 检查用户账号密码是否正确
     * @param urlStr 接口url
     * @param user_phone    用户输入的帐号
     * @param user_password     用户输入的密码
     * @return
     */
    public static String checkuser(String urlStr,String user_phone,String user_password){
        String params = "{\"user_phone\":" +user_phone +",\"user_password\":" + user_password+  "}";
        try {
            URL url=new URL(urlStr);
            HttpURLConnection connect=(HttpURLConnection)url.openConnection();
            connect.setDoInput(true);
            connect.setDoOutput(true);
            connect.setRequestMethod("POST");
            connect.setUseCaches(false);
            connect.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            OutputStream outputStream = connect.getOutputStream();
            outputStream.write(params.getBytes());
            int response = connect.getResponseCode();
            if (response== HttpURLConnection.HTTP_OK)
            {
                System.out.println(response);
                InputStream input=connect.getInputStream();
                BufferedReader in = new BufferedReader(new InputStreamReader(input));
                String line = null;
                StringBuffer sb = new StringBuffer();
                while ((line = in.readLine()) != null) {
                    sb.append(line);
                }
                return sb.toString();
            }
            else {
                System.out.println(response);
                return " ";
            }
        } catch (Exception e) {
            Log.e("e:", String.valueOf(e));
            return e.toString();
        }
    }

    /**
     * 用户重新设置密码
     * @param urlStr    接口uel
     * @param user_password     用户输入的新密码
     * @param user_id      用户id
     * @return
     */
    public static String rsetpassword(String urlStr,String user_password,int user_id){
        String params = "{\"user_password\":" +user_password +",\"user_id\":" + user_id+  "}";
        try {
            URL url=new URL(urlStr);
            HttpURLConnection connect=(HttpURLConnection)url.openConnection();
            connect.setDoInput(true);
            connect.setDoOutput(true);
            connect.setRequestMethod("POST");
            connect.setUseCaches(false);
            connect.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            OutputStream outputStream = connect.getOutputStream();
            outputStream.write(params.getBytes());
            int response = connect.getResponseCode();
            if (response== HttpURLConnection.HTTP_OK)
            {
                System.out.println(response);
                InputStream input=connect.getInputStream();
                BufferedReader in = new BufferedReader(new InputStreamReader(input));
                String line = null;
                System.out.println(connect.getResponseCode());
                StringBuffer sb = new StringBuffer();
                while ((line = in.readLine()) != null) {
                    sb.append(line);
                }
                return sb.toString();
            }
            else {
                System.out.println(response);
                return " ";
            }
        } catch (Exception e) {
            Log.e("e:", String.valueOf(e));
            return e.toString();
        }
    }

    /**
     * 获得书籍信息
     * @param urlStr    接口url
     * @param id    书籍id
     * @return
     */
    public static String getbookinfo(String urlStr,int id){
        String params = "{\"book_id\":"+id+"}";
        try {
            URL url=new URL(urlStr);
            HttpURLConnection connect=(HttpURLConnection)url.openConnection();
            connect.setDoInput(true);
            connect.setDoOutput(true);
            connect.setRequestMethod("POST");
            connect.setUseCaches(false);
            connect.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            OutputStream outputStream = connect.getOutputStream();
            outputStream.write(params.getBytes());
            int response = connect.getResponseCode();
            if (response== HttpURLConnection.HTTP_OK)
            {
                System.out.println(response);
                InputStream input=connect.getInputStream();
                BufferedReader in = new BufferedReader(new InputStreamReader(input));
                String line = null;
                System.out.println(connect.getResponseCode());
                StringBuffer sb = new StringBuffer();
                while ((line = in.readLine()) != null) {
                    sb.append(line);
                }
                return sb.toString();
            }
            else {
                System.out.println(response);
                return "";
            }
        } catch (Exception e) {
            System.out.println(e.toString());
            return "";
        }
    }

    /**
     * 获得文章信息
     * @param urlStr    接口url
     * @param id    文章id
     * @return
     */
    public static String getarticleinfo(String urlStr,int id){
        String params = "{\"article_id\":"+id+"}";
        try {
            URL url=new URL(urlStr);
            HttpURLConnection connect=(HttpURLConnection)url.openConnection();
            connect.setDoInput(true);
            connect.setDoOutput(true);
            connect.setRequestMethod("POST");
            connect.setUseCaches(false);
            connect.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            OutputStream outputStream = connect.getOutputStream();
            outputStream.write(params.getBytes());
            int response = connect.getResponseCode();
            if (response== HttpURLConnection.HTTP_OK)
            {
                System.out.println(response);
                InputStream input=connect.getInputStream();
                BufferedReader in = new BufferedReader(new InputStreamReader(input));
                String line = null;
                System.out.println(connect.getResponseCode());
                StringBuffer sb = new StringBuffer();
                while ((line = in.readLine()) != null) {
                    sb.append(line);
                }
                return sb.toString();
            }
            else {
                System.out.println(response);
                return "";
            }
        } catch (Exception e) {
            System.out.println(e.toString());
            return "";
        }
    }

    /**
     * 添加书籍到书架
     * @param urlStr 接口url
     * @param user_id   用户id
     * @param book_id   书籍id
     * @return
     */
    public static String addbook(String urlStr,int user_id,int book_id){
        String params = "{\"user_id\":" +user_id +",\"book_id\":" +book_id+  "}";
        try {
            URL url=new URL(urlStr);
            HttpURLConnection connect=(HttpURLConnection)url.openConnection();
            connect.setDoInput(true);
            connect.setDoOutput(true);
            connect.setRequestMethod("POST");
            connect.setUseCaches(false);
            connect.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            OutputStream outputStream = connect.getOutputStream();
            outputStream.write(params.getBytes());
            int response = connect.getResponseCode();
            if (response== HttpURLConnection.HTTP_OK)
            {
                System.out.println(response);
                InputStream input=connect.getInputStream();
                BufferedReader in = new BufferedReader(new InputStreamReader(input));
                String line = null;
                System.out.println(connect.getResponseCode());
                StringBuffer sb = new StringBuffer();
                while ((line = in.readLine()) != null) {
                    sb.append(line);
                }
                return sb.toString();
            }
            else {
                System.out.println(response);
                return "not exsits";
            }
        } catch (Exception e) {
            Log.e("e:", String.valueOf(e));
            return "internet errar";
        }
    }

    /**
     * 添加文章到收藏夹
     * @param urlStr    接口url
     * @param user_id   用户id
     * @param book_id   文章id
     * @return
     */
    public static String addarticle(String urlStr,int user_id,int book_id){
        String params = "{\"user_id\":" +user_id +",\"article_id\":" +book_id+  "}";
        try {
            URL url=new URL(urlStr);
            HttpURLConnection connect=(HttpURLConnection)url.openConnection();
            connect.setDoInput(true);
            connect.setDoOutput(true);
            connect.setRequestMethod("POST");
            connect.setUseCaches(false);
            connect.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            OutputStream outputStream = connect.getOutputStream();
            outputStream.write(params.getBytes());
            int response = connect.getResponseCode();
            if (response== HttpURLConnection.HTTP_OK)
            {
                System.out.println(response);
                InputStream input=connect.getInputStream();
                BufferedReader in = new BufferedReader(new InputStreamReader(input));
                String line = null;
                System.out.println(connect.getResponseCode());
                StringBuffer sb = new StringBuffer();
                while ((line = in.readLine()) != null) {
                    sb.append(line);
                }
                return sb.toString();
            }
            else {
                System.out.println(response);
                return "not exsits";
            }
        } catch (Exception e) {
            Log.e("e:", String.valueOf(e));
            return "internet errar";
        }
    }

    /**
     * 获得某一类图书资源
     * @param book_tap  图书分类
     * @return
     */
    public static String gettypebook(String book_tap){
        String h="http://122.114.237.201/getbook/classifiedbooks";
        JSONObject object=new JSONObject();

        try {
            object.put("book_tap",book_tap);

            String content = String.valueOf(object);
            URL url=new URL(h);
            HttpURLConnection connect=(HttpURLConnection)url.openConnection();
            connect.setDoInput(true);
            connect.setDoOutput(true);
            connect.setRequestMethod("POST");
            connect.setUseCaches(false);
            connect.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            OutputStream outputStream = connect.getOutputStream();
            outputStream.write(content.getBytes());
            int response = connect.getResponseCode();
            System.out.println(connect);
            if (response== HttpURLConnection.HTTP_OK)
            {
                System.out.println(response);
                InputStream input=connect.getInputStream();
                BufferedReader in = new BufferedReader(new InputStreamReader(input));
                String line = null;
                System.out.println(connect.getResponseCode());
                StringBuffer sb = new StringBuffer();
                while ((line = in.readLine()) != null) {
                    sb.append(line);
                }
                return sb.toString();
            }
            else {
                System.out.println(response);
                return "not exsits";
            }
        } catch (Exception e) {
            Log.e("e:", String.valueOf(e));
            return "internet errar";
        }
    }

    /**
     * 获得搜索结果
     * @param bookName  用户输入的书籍关键字
     * @return
     */
    public static String getsearchresult(String bookName){
        String h="http://122.114.237.201/getbook/search";
        JSONObject object=new JSONObject();

        try {
            object.put("bookName",bookName);

            String content = String.valueOf(object);
            URL url=new URL(h);
            HttpURLConnection connect=(HttpURLConnection)url.openConnection();
            connect.setDoInput(true);
            connect.setDoOutput(true);
            connect.setRequestMethod("POST");
            connect.setUseCaches(false);
            connect.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            OutputStream outputStream = connect.getOutputStream();
            outputStream.write(content.getBytes());
            int response = connect.getResponseCode();
            System.out.println(connect);
            if (response== HttpURLConnection.HTTP_OK)
            {
                System.out.println(response);
                InputStream input=connect.getInputStream();
                BufferedReader in = new BufferedReader(new InputStreamReader(input));
                String line = null;
                System.out.println(connect.getResponseCode());
                StringBuffer sb = new StringBuffer();
                while ((line = in.readLine()) != null) {
                    sb.append(line);
                }
                return sb.toString();
            }
            else {
                System.out.println(response);
                return "not exsits";
            }
        } catch (Exception e) {
            Log.e("e:", String.valueOf(e));
            return "internet errar";
        }
    }

    /**
     * 获得用户信息
     * @param urlStr    接口url
     * @param id    用户id
     * @return
     */
    public static String getuserinfo(String urlStr,int id){
        String params = "{\"user_id\":"+id+"}";
        try {
            URL url=new URL(urlStr);
            HttpURLConnection connect=(HttpURLConnection)url.openConnection();
            connect.setDoInput(true);
            connect.setDoOutput(true);
            connect.setRequestMethod("POST");
            connect.setUseCaches(false);
            connect.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            OutputStream outputStream = connect.getOutputStream();
            outputStream.write(params.getBytes());
            int response = connect.getResponseCode();
            if (response== HttpURLConnection.HTTP_OK)
            {
                System.out.println(response);
                InputStream input=connect.getInputStream();
                BufferedReader in = new BufferedReader(new InputStreamReader(input));
                String line = null;
                System.out.println(connect.getResponseCode());
                StringBuffer sb = new StringBuffer();
                while ((line = in.readLine()) != null) {
                    sb.append(line);
                }
                return sb.toString();
            }
            else {
                System.out.println(response);
                return "";
            }
        } catch (Exception e) {
            System.out.println(e.toString());
            return "";
        }
    }
}
