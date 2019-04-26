import java.io.*;
import java.util.*;

class BikeAvailability {
  private Date clock;
  private boolean available;
  private int bikeNum = 0;
  private static int[][] bikeMap = new int[10][10];
  private final int[][] saved;
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

    if (saved == null) {
      System.out.println("hello");
      saved = new int[10][10];
      for (i=0; i<10; i++) {
        for (j=0; j<10; j++) {
          bikeMap[i][j] = 3;
          returnedBike = new Bike("null", i, j, initTime);
          returnedBike.status = Rental.Returned;
          storage[i][j] = returnedBike;
        }
      }
    }
    else {
      for (i=0; i<10; i++) {
        for (j=0; j<10; j++) {
          if (bikeMap[i][j] == 3) {
            returnedBike = new Bike("null", i, j, initTime);
            returnedBike.status = Rental.Returned;
            storage[i][j] = returnedBike;
          }
          else if (bikeMap[i][j] == 1) System.out.println("second time running");
        }
      }
    }
  }

  public void returnAll(Date initTime) {
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

  public Bike hireBike(String bikeName, int x, int y, Date eventTime) {
    // bikeMap[x][y] = 1;
    Bike newBike = new Bike(bikeName, x, y, eventTime);

    newBike.status = Rental.Rent;
    storage[x][y] = newBike;

    return newBike;
  }

  public void printMap() {
    int i;
    int j;


    for (i=0; i<storage.length; i++) {
      for (j=0; j<storage[i].length; j++) {
        if (storage[i][j].status == Rental.Returned) {
          bikeMap[i][j] = 3;
        }
        else if (storage[i][j].status == Rental.Rent) {
          bikeMap[i][j] = 1;
        }
        if (storage[i][j].status == Rental.Returned) {
          System.out.printf("3 ");
        }
        else if (storage[i][j].status == Rental.Rent) {
          System.out.printf("1 ");
        }
        // else System.out.printf(bikeMap[i][j] + " ");
      }
      System.out.println();
    }
  }

  public void returnBike(int x, int y) {
    bikeMap[x][y] = 0;
  }

  public int[][] save(int[][] map) {
    int[][] recall = new int[map.length][];
    int i;
    for (i=0; i<map.length; i++) {
      recall[i] = Arrays.copyOf(map[i], map[i].length);
    }
    return recall;
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
        if (storage[i][j].status == Rental.Returned) {
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
    // int[][] retrieved = new int[10][10];

    example.initBikes(now);

    System.out.printf("What bike do you want to rent? ");
    String userBike = userInput.nextLine();

    sample = example.checkBike();
    sample = example.hireBike(userBike, sample.row, sample.column, now);
    // saved = example.save(bikeMap);
    // for(int i =0; i<saved.length; i++) {
    //   for (int j=0; j<saved[i].length; j++) {
    //     System.out.printf(saved[i][j] + " ");
    //   }
    //   System.out.println();
    // }

    example.printMap();
    // example.checkBike();
  }
}
