import java.io.*;
import java.util.*;
import java.lang.StringBuilder;

class BikeAvailability {
  private Date clock;
  private boolean available;
  private int bikeNum = 0;
  private static int[][] bikeMap = new int[10][10];
  private int[][] saved;
  private Bike[][] storage = new Bike[10][10];

  public static enum Rental {
    Rent, Returned, New;
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
    Bike newOne;

    for (i=0; i<bikeMap.length; i++) {
      for (j=0; j<bikeMap[i].length; j++) {
        bikeMap[i][j] = 3;
        newOne = new Bike("new", i, j, initTime);
        newOne.status = Rental.New;
        storage[i][j] = newOne;
      }
    }
  }

  public void returnAll(Date initTime) {
    int i = 0;
    int j = 0;
    Bike returnedBike;

    for (i=0; i<bikeMap.length; i++) {
      for (j=0; j<bikeMap[i].length; j++) {
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

  public void returnBike(String bikeName) {
    int i;
    int j;
    int row;
    int column;

    for (i=0; i<storage.length; i++) {
      for (j=0; j<storage[i].length; j++) {
        if (bikeName.equals(storage[i][j].label)) {
          System.out.println("found");
          row = i;
          column = j;
          storage[row][column].status = Rental.Returned;
          storage[row][column].label = "null";
          bikeMap[row][column] = 0;
        }
      }
    }
  }

  public void save() {
    StringBuilder arrayFile = new StringBuilder();
    int i;
    int j;
    BufferedWriter fileWriter;

    for(i=0; i<bikeMap.length; i++) {
      for(j=0; j<bikeMap[i].length; j++) {
        arrayFile.append(bikeMap[i][j] + "");
        if (j < bikeMap.length - 1) {
          arrayFile.append(", ");
        }
      }
      arrayFile.append("\n");
    }
    try {
      fileWriter = new BufferedWriter(new FileWriter("saved.txt"));
      fileWriter.write(arrayFile.toString());
      fileWriter.close();
    } catch(IOException err) {
      System.err.println(err);
    }
  }

  public int[][] load() {
    String fileToLoad = "saved.txt";

    int[][] savedMap = new int[10][10];
    BufferedReader fileReader;
    String data = "";
    int row = 0;
    // int count = 0;

    try {
      fileReader = new BufferedReader(new FileReader(fileToLoad));

      while ((data = fileReader.readLine()) != null) {
        String[] columns = data.split(", ");
        int column = 0;
        for (String bit : columns) {
          // count++;
          // System.out.println(count);
          savedMap[row][column] = Integer.parseInt(bit);
          if (savedMap[row][column] == 3) storage[row][column].status = Rental.Returned;
          else storage[row][column].status = Rental.Rent;
          // System.out.println(savedMap[row][column]);
          column++;
        }
        row++;
      }
      fileReader.close();
    } catch (FileNotFoundException err) {
      System.err.println(err);
    } catch (IOException err) {
      System.err.println(err);
    }
    return savedMap;
  }

  public Bike checkBike() {
    int row = 0;
    int column = 0;
    int i;
    int j;
    boolean checked = false;

    for (i=0; i<storage.length; i++) {
      if (checked) break;
      for (j=0; j<storage[i].length; j++) {
        if (storage[i][j].status == Rental.Returned || storage[i][j].status == Rental.New) {
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
    while(true) {
      System.out.println("Enter any commands: ");
      String command = userInput.nextLine();

      if (command.equals("save")) example.save();
      else if (command.equals("hire")) {
        System.out.printf("What bike do you want to rent? ");
        String userBike = userInput.nextLine();
        sample = example.checkBike();
        sample = example.hireBike(userBike, sample.row, sample.column, now);
      }
      else if (command.equals("load")) {
        bikeMap = example.load();
      }
      else if (command.equals("return")) {
        example.returnBike("me");
      }
      else if (command.equals("print")) example.printMap();
      else if (command.equals("exit")) System.exit(1);
      else System.out.println("Wrong comment");
    }
  }
}
