package PageObjects;

import Utility.BasePage;
import com.opencsv.CSVWriter;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class JobPage extends BasePage {

    @FindBy(xpath = "//div[@class='lteri']/div[2]/div/div/div/div/div/div/div/h2")
    public WebElement jobTitle;

    @FindBy(xpath = "//div[@class='lteri']/div[2]/div/div[1]/div/div/div[4]/div/span")
    public WebElement jobDescription1;

    @FindBy(xpath = "//div[@class='lteri']/div[2]/div/div[1]/div/div/div[4]/div/span/span[2]")
    public WebElement jobDescription2;

    List<String[]> list= new ArrayList<>();

    CSVWriter writer = new CSVWriter(new FileWriter("output.csv"));

    public JobPage() throws IOException {
        PageFactory.initElements(getDriver(), this);
    }

    public void iterateOverList() throws IOException {
        List<WebElement> listJobs;
        String stTitle = null;
        String stDesc_1;
        String stDesc_2;
        String stDesc = null;
        int initSize;
        int size;
        listJobs = getDriver().findElements(By.xpath("//div/ul/li"));

        System.out.println("initial size of JobList: " + listJobs.size());
        initSize = listJobs.size();
        JavascriptExecutor js = (JavascriptExecutor) getDriver();
        int i=0;

        size = initSize;
        boolean readyToAdd = false;

        while (i<size-1) {
            System.out.println("iter-" + i);
            clickOnElement(listJobs.get(i), 5);
            try {
                stTitle = jobTitle.getText();
                stDesc_1 = jobDescription1.getText();
                stDesc_2 = jobDescription2.getAttribute("textContent");
                stDesc = stDesc_1 + stDesc_2;
                readyToAdd = true;
            } catch (Exception e) {
                System.out.println("SKIPPING this job posting");
            }
            
            System.out.println(stTitle);
            if (readyToAdd) {
                list.add(new String[]{stTitle, stDesc});
            }

            js.executeScript("arguments[0].scrollIntoView();", listJobs.get(i));
            i++;
            listJobs = getDriver().findElements(By.xpath("//div/ul/li"));
            size = listJobs.size();
            System.out.println("current size: " + size);
            System.out.println("************************************");
        }
        writer.writeAll(list);
        writer.flush();
    }
}
