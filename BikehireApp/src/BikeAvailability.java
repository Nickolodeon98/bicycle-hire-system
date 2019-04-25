import java.io.*;
import java.util.*;

class BikeAvailability {
  private Date clock;
  private boolean available;
  private int bikeNum = 0;
  private int[][] bikeMap = {{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}};

  private Bike[][] storage = new Bike[10][10];

  public static enum Rental {
    Rent, Returned;
  }
  public static class Bike {
    public String label;
    public int row;
    public int column;
    public Date rentalTime;
    public Rental status;

    public Bike(String name, int xCoord, int yCoord, Date time) {
      this.row = xCoord;
      this.column = yCoord;
      this.rentalTime = time;
      this.label = name;
    }
  }

  public void initBikes(Date initTime) {
    int i = 0;
    int j = 0;
    Bike returnedBike;

    for (i=0; i<10; i++) {
      for (j=0; j<10; j++) {
        returnedBike = new Bike("null", i, j, initTime);
        returnedBike.status = Rental.Returned;
        storage[i][j] = returnedBike;
      }
    }
  }

  public void returnAll(Date initTime) {
    int i = 0;
    int j = 0;
    Bike returnedBike;

    for (i=0; i<10; i++) {
      for (j=0; j<10; j++) {
        bikeMap[i][j] = 0;
        returnedBike = new Bike("null", i, j, initTime);
        returnedBike.status = Rental.Returned;
        storage[i][j] = returnedBike;
      }
    }
  }

  public Bike hireBike(String bikeName, int x, int y, Date eventTime) {
    bikeMap[x][y] = 1;
    Bike newBike = new Bike(bikeName, x, y, eventTime);

    newBike.status = Rental.Rent;
    storage[x][y] = newBike;

    return newBike;
  }

  public void printMap() {
    int i;
    int j;

    for (i=0; i<bikeMap.length; i++) {
      for (j=0; j<bikeMap[i].length; j++) {
        System.out.printf(bikeMap[i][j] + " ");
      }
      System.out.println();
    }
  }

  public void returnBike(int x, int y) {
    bikeMap[x][y] = 0;
  }

  public Bike checkBike() {
    int row = 0;
    int column = 0;
    int i;
    int j;
    boolean checked = false;

    for (i=0; i<10; i++) {
      if (checked) break;
      for (j=0; j<10; j++) {
        if (bikeMap[i][j] == 0) {
          available = true;
          bikeNum++;
          row = i;
          column = j;
          checked = true;
          break;
        }
      }
    }

    // System.out.println(storage[row][column].label);
    // System.out.println(storage[row][column].rentalTime);

    if (!available) {
      System.out.println("Bike not available at the moment");
    } else {
      System.out.println("Bike available at (" + row + ", " + column + ")");
    }

    return storage[row][column];
  }

  public static void main(String[] args) {
    BikeAvailability example = new BikeAvailability();
    Bike sample;
    Date now = new Date();
    Scanner userInput = new Scanner(System.in);

    example.initBikes(now);

    System.out.printf("What bike do you want to rent? ");
    String userBike = userInput.nextLine();

    sample = example.checkBike();
    example.hireBike(userBike, sample.row, sample.column, now);



    example.printMap();
    // example.checkBike();
  }
}
