import java.io.*;
import java.util.*;

class bikeAvailability {
  private Date clock;
  private boolean available;
  private int bikeNum = 0;
  private int[][] bikeMap = new int[10][10];

  public static enum Rental {
    Rent, Returned
  }
  public static class bike {
    public char label;
    public int row;
    public int column;
    public Date rentalTime;
    public Rental status;
  }


  public void initBikes() {
    int i = 0
    int j = 0;
    for (i=0; i<10; i++) {
      for (j=0; j<10; j++) {
        bikeMap[i][j] = 0;
      }
    }
  }

  public void hireBike(int x, int y) {
    bikeMap[x][y] = 1;
  }

  public void returnBike(int x, int y) {
    bikeMap[x][y] = 0;
  }



  public void checkBike() {
    int row;
    int column;

    for (i=0; i<10; i++) {
      for (j=0; j<10; j++) {
        if (bikeMap[i][j] == 0) {
          available = true;
          bikeNum++;
          row = i;
          column = j;
        }
      }
    }
    if (!available) {
      System.out.println("Bike not available at the moment");
    } else {
      System.out.println("Bike available at (" + row + ", " + column + ")");
    }
  }

  public static void main(String[] args) {

  }
}
