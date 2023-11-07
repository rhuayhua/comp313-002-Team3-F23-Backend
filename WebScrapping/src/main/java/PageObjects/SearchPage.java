package PageObjects;

import Utility.BasePage;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

public class SearchPage extends BasePage {

    @FindBy(xpath = "//div/*/textarea")
    public WebElement searchBox;

    @FindBy(xpath = "//div/center/input[@name='btnK']")
    public WebElement searchBtn;

    @FindBy(xpath = "//span[contains(.,'more jobs')]")
    public WebElement moreJobsBtn;

    public SearchPage() {
        PageFactory.initElements(getDriver(), this);
    }

    public void enterJobAndClickSearch(String jobName, String location) {
        typeInElement(searchBox, jobName + " jobs in " + location +  Keys.ENTER, 5);
        ///clickOnElement(searchBtn, 50);
        clickOnElement(moreJobsBtn, 5);
    }

}
