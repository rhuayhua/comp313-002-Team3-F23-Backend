package Utility;

import io.qameta.allure.Step;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.FluentWait;
import org.openqa.selenium.support.ui.Wait;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import java.time.Duration;

public class BasePage extends Listener {

    private static ThreadLocal<RemoteWebDriver> driver = new ThreadLocal<>();
    public static WebDriver getDriver() {
        return driver.get();
    }

    public void setDriverToNull() {
        printDebugMessage("Setting driver to NULL after quitting");
        driver.set(null);
    }

    public void openBrowserAndNavigateToGoogle(String executionType, String browserName) {
        printDebugMessage("BasePage.openBrowser");
        if (executionType.equals("Local")) {
            switch (browserName) {
                case "Firefox":
                    System.setProperty("webdriver.gecko.driver", "C://Users//rhuay//Documents//Selenium//BrowserDriver//geckodriver.exe");
                    driver.set(new FirefoxDriver());
                    break;
                default:
                    System.setProperty("webdriver.chrome.driver", "C://Users//rhuay//Documents//Selenium//BrowserDriver//chromedriver.exe");
                    ChromeOptions options = new ChromeOptions();
                    options.addArguments("--remote-allow-origins=*");
                    driver.set(new ChromeDriver(options));
                    break;
            }

        }

        getDriver().manage().timeouts().implicitlyWait(Duration.ofSeconds(2));
        getDriver().manage().timeouts().pageLoadTimeout(Duration.ofSeconds(60));
        getDriver().manage().window().maximize();
        getDriver().manage().deleteAllCookies();
        getDriver().get("https://www.google.com");
    }

    public void highlightElement(WebElement element) {
        JavascriptExecutor jse = (JavascriptExecutor) driver.get();
        jse.executeScript("arguments[0].style.border='2px solid yellow'", element);
    }

    @Step("Wait and Assert element is visible")
    public void findVisibleElementWithExplicitWait(WebElement element, long sec) {
        try {
            WebDriverWait wait = new WebDriverWait(getDriver(), Duration.ofSeconds(sec));
            wait.until(ExpectedConditions.visibilityOf(element));
            highlightElement(element);
        } catch (Exception e) {
            printDebugMessage("ERROR finding element: " + element.toString());
        }
        Assert.assertTrue(element.isDisplayed());
    }

    @Step("Wait and click on element")
    public void clickOnElement(WebElement element, long sec) {
        boolean isClicked = false;
        findVisibleElementWithExplicitWait(element, 5);
        try {
            Wait<WebDriver> wait = new FluentWait<>(getDriver())
                    .withTimeout(Duration.ofSeconds(sec))
                    .pollingEvery(Duration.ofMillis(500))
                    .ignoring(ElementNotInteractableException.class);
            wait.until(d -> {
                element.click();
                return true;
            });
            isClicked = true;
        } catch (Exception e) {
            printDebugMessage("ERROR clicking on element: " + element.toString());
        }
        Assert.assertTrue(isClicked);
    }

    @Step("Wait and type in element")
    public void typeInElement(WebElement element, String text, long sec) {
        boolean dataTyped = false;
        findVisibleElementWithExplicitWait(element, 5);
        try {
            Wait<WebDriver> wait = new FluentWait<>(getDriver())
                    .withTimeout(Duration.ofSeconds(sec))
                    .pollingEvery(Duration.ofMillis(500))
                    .ignoring(ElementNotInteractableException.class);
            wait.until(d -> {
                element.sendKeys(text);
                return true;
            });
            dataTyped = true;
        } catch (Exception e) {
            printDebugMessage("ERROR typing in element: " + element.toString());
        }
        Assert.assertTrue(dataTyped);
    }

}
