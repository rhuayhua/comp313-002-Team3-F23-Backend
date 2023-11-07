package PageObjectSteps;

import Utility.BasePage;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Parameters;
import java.io.IOException;

public class BaseTest extends BasePage {

    public ScrappingSteps scrappingSteps;

    public void initializedSteps() throws IOException {
        scrappingSteps = new ScrappingSteps();
    }

    @Parameters({"ExecutionType","BrowserName"})
    @BeforeClass(alwaysRun = true)
    public void testSetup(String ExecutionType, String BrowserName ) throws IOException {
        printDebugMessage("Execution type is: " + ExecutionType);
        printDebugMessage("Browser name is: " + BrowserName);
        openBrowserAndNavigateToGoogle(ExecutionType, BrowserName);
        initializedSteps();
    }

    @AfterClass(alwaysRun = true)
    public void tearDown() {
        printDebugMessage("Test tear down");
        if (getDriver()!=null) {
            printDebugMessage("Clearing driver - SessionID: " + ((RemoteWebDriver) getDriver()).getSessionId());
            getDriver().quit();
            setDriverToNull();
            printDebugMessage("Driver cleared");
        }
    }

}
