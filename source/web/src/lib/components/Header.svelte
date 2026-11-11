<script>
    import { Book, ExternalLink, FolderGit2 } from "@lucide/svelte";
    import IconButton from "./IconButton.svelte";
    import ToolButton from "./ToolButton.svelte";

</script>
<div class="navbar-container">
    <div class="top-navbar">
        <div class="top-navbar-logo-title-container">
            <a href="https://www.helmholtz-berlin.de/" target="_blank">
                <img src="/images/hzb-logo-a4-invers.svg" id="hzb-icon" alt="HZB-Logo inverse"/>
            </a>
            <h1>RAYX-WebApp</h1>
        </div>
        <div class="top-navbar-link-buttons">
            <IconButton
                text="How to use"
                icon={Book}
                link="https://github.com/hz-b/rayx-webapp/wiki"
            />
            <IconButton
                text="GitHub Repository"
                icon={FolderGit2}
                link="https://github.com/hz-b/rayx-webapp"
            />  <!--TODO: Needs to be changed to real GitHub Icon-->
            <IconButton
                text="RAYX"
                icon={ExternalLink}
                link="https://github.com/hz-b/rayx"
            />
        </div>
    </div>
    <div class="bottom-navbar">
        <!--Available tool-pages-->
        <ToolButton text="Reflectivity" link="https://www.nyan.cat/" isSelected={true}/>
        <ToolButton text="Beamline Tracer" link="https://www.nyan.cat/"/>
    </div>
</div>

<style>
    .navbar-container{
        background: linear-gradient(to right, var(--color-primary) 50%, vaR(--color-secondary));;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
        padding-right: 1rem;
    }

    .top-navbar{
        display: flex;
        flex-flow: row;
        justify-content: space-between;
    }

    .top-navbar-logo-title-container {
        display: flex;
        flex-flow: row;
    }

    .top-navbar-link-buttons{
        display: flex;
        align-items: center;
    }

    .bottom-navbar{
        padding: 0 1rem;
    }

    #hzb-icon {
        width: 12rem;
    }

    h1 {
        white-space: nowrap;
    }
</style>
