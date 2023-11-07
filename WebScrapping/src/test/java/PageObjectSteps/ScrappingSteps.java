package PageObjectSteps;

import PageObjects.JobPage;
import PageObjects.SearchPage;
import Utility.BasePage;
import java.io.IOException;

public class ScrappingSteps extends BasePage {

    public JobPage jobPage;
    public SearchPage searchPage;

    public ScrappingSteps() throws IOException {
        jobPage = new JobPage();
        searchPage = new SearchPage();
    }

    public void getData(String role, String location) throws InterruptedException, IOException {
        searchPage.enterJobAndClickSearch(role, location);
        jobPage.iterateOverList();
    }

}
