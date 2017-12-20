// --------------------------------------------------------------------
// This simple example shows how to do basic animation
// using C++
//

#include "vtkAnimationCue.h"
#include "vtkAnimationScene.h"
#include "vtkCommand.h"
#include "vtkRenderer.h"
#include "vtkSphereSource.h"
#include "vtkPolyDataMapper.h"
#include "vtkActor.h"
#include "vtkRenderer.h"
#include "vtkRenderWindow.h"
#include "vtkRenderWindowInteractor.h"
#include <unistd.h>
class CueAnimator
{
public:
   CueAnimator()
     {
     this->SphereSource = 0;
     this->Mapper = 0;
     this->Actor = 0;
     }
   ~CueAnimator()
     {
     this->Cleanup();
     }
   void StartCue(vtkAnimationCue::AnimationCueInfo* info, vtkRenderer* ren)
     {
     cout <<"*** IN StartCue "<< endl;
     this->SphereSource = vtkSphereSource::New();
     this->SphereSource->SetRadius(0.5);

     this->Mapper = vtkPolyDataMapper::New();
     this->Mapper->SetInput(this->SphereSource->GetOutput());

     this->Actor = vtkActor::New();
     this->Actor->SetMapper(this->Mapper);

     ren->AddActor(this->Actor);
     ren->ResetCamera();
     ren->Render();
     }

   void Tick(vtkAnimationCue::AnimationCueInfo* info, vtkRenderer* ren)
     {
     double newradius = 0.1 + ((double)(info->CurrentTime - 
info->StartTime)/
       (double)(info->EndTime - info->StartTime)) * 1;
     this->SphereSource->SetRadius(newradius);
     this->SphereSource->Update();
     ren->Render();
     }
   void EndCue(vtkAnimationCue::AnimationCueInfo *info, vtkRenderer* ren)
     {
     ren->RemoveActor(this->Actor);
     this->Cleanup();
     }
protected:
   vtkSphereSource* SphereSource;
   vtkPolyDataMapper* Mapper;
   vtkActor* Actor;
   void Cleanup()
     {
     if (this->SphereSource)
       {
       this->SphereSource->Delete();
       }
     this->SphereSource = 0;
     if (this->Mapper)
       {
       this->Mapper->Delete();
       }
     this->Mapper = 0;
     if (this->Actor)
       {
       this->Actor->Delete();
       }
     this->Actor = 0;
     }
};
class vtkAnimationCueObserver : public vtkCommand
{
public:
   static vtkAnimationCueObserver* New()
     {
     return new vtkAnimationCueObserver;
     }

   virtual void Execute(vtkObject* caller, unsigned long event,
     void* calldata)
     {
     if (this->Animator && this->Renderer)
       {
       switch(event)
         {
       case vtkCommand::StartAnimationCueEvent:
         Animator->StartCue((vtkAnimationCue::AnimationCueInfo*) calldata,
           this->Renderer);
         break;
       case vtkCommand::EndAnimationCueEvent:
         Animator->EndCue((vtkAnimationCue::AnimationCueInfo*) calldata,
           this->Renderer);
         break;
       case vtkCommand::AnimationCueTickEvent:
         Animator->Tick((vtkAnimationCue::AnimationCueInfo*) calldata,
           this->Renderer);
         break;
         }
       }
     if (this->RenWin)
       {
       this->RenWin->Render();
       }
     }
   vtkRenderer* Renderer;
   vtkRenderWindow* RenWin;
   CueAnimator* Animator;
protected:
     vtkAnimationCueObserver()
       {
       this->Renderer = 0;
       this->Animator = 0;
       this->RenWin = 0;
       }

};




int main(int argc, char* argv[])
{
   // Create the graphics structure. The renderer renders into the
   // render window.
   vtkRenderer *ren1 = vtkRenderer::New();
   vtkRenderWindow *renWin = vtkRenderWindow::New();
   renWin->AddRenderer(ren1);
   renWin->Render();

   // Create an Animation Scene
   vtkAnimationScene* scene = vtkAnimationScene::New();
   if (argc >= 2 && strcmp(argv[1],"real") == 0)
     {
     scene->SetModeToRealTime();
     }
   else
     {
     scene->SetModeToSequence();
     }
   scene->SetLoop(0);
   scene->SetFrameRate(5);
   scene->SetStartTime(3);
   scene->SetEndTime(20);

   // Create an Animation Cue.
   vtkAnimationCue* cue1 = vtkAnimationCue::New();
   cue1->SetStartTime(5);
   cue1->SetEndTime(13);
   scene->AddCue(cue1);

   // Create cue animator;
   CueAnimator animator;

   // Create Cue observer.
   vtkAnimationCueObserver* observer = vtkAnimationCueObserver::New();
   observer->Renderer = ren1;
   observer->Animator = &animator;
   observer->RenWin = renWin;
   cue1->AddObserver(vtkCommand::StartAnimationCueEvent, observer);
   cue1->AddObserver(vtkCommand::EndAnimationCueEvent, observer);
   cue1->AddObserver(vtkCommand::AnimationCueTickEvent, observer);

   scene->Play();
   scene->Stop();

   ren1->Delete();
   renWin->Delete();
   scene->Delete();
   cue1->Delete();
   observer->Delete();
   return 0;
}
// --------------------------------------------------------------------
